
class And {
    constructor(left, right) {
        this.left = left
        this.right = right
    }

    toString() {
        return `${this.left} && ${this.right}`
    }
}

class Or {
    constructor(left, right) {
        this.left = left
        this.right = right
    }

    toString() {
        return `${this.left} || ${this.right}`
    }
}

class Group {
    constructor(expr) {
        this.expr = expr
    }
    toString() {
        return `(${this.expr})`
    }
}

class Method {
    constructor(name, args) {
        this.name = name
        this.args = args
    }
    toString() {
        return `${this.name}(${this.args.join(", ")})`
    }
}

function* tokenizer(s, parsers, ignoreSpaces = true) {
    while (s) {
        if (ignoreSpaces) {
            s = s.trim()
        }
        let token = null;
        for (const [name, parser] of Object.entries(parsers)) {
            const r = parser.exec(s)
            if (r && r.index == 0) {
                token = {
                    value: r[0],
                    type: name,
                }
            }
        }
        if (token == null) {
            throw "Invalid rule"
        }
        yield token
        s = s.substr(token.value.length);
    }
}

function getAssert(tokens, ...valids) {
    const token = tokens.next().value

    if (!token) {
        throw `Invalid syntax, missing token`
    }

    if (valids.length) {
        if (!valids.find(a => a == token.type)) {
            throw `Invalid syntax, expected ${valids}, got ${token.type}`
        }
    }
    return token
}

function PathPrefix(tokens) {
    let token;
    getAssert(tokens, "OPENPAR")
    do {
        getAssert(tokens, "STRING")
    } while (true)
}



function parseMethod(methodName, tokens) {
    getAssert(tokens, "OPENPAR")
    let token;
    const args = []
    do {
        token = getAssert(tokens)

        if (token.type == "STRING") {
            args.push(token.value)
            token = getAssert(tokens, "CLOSEPAR", "COMMA")
        }
    } while (token.type != "CLOSEPAR");
    return new Method(methodName, args)
}

function parseGroup(tokens) {
    const [expr, token] = parseExpression(tokens)
    if (token.type != "CLOSEPAR") throw "Missing closing parenthese"
    return new Group(expr)
}



function parseExpression(tokens) {
    let token = getAssert(tokens, "OPENPAR", "METHOD")

    let expr = null

    switch (token.type) {
        case "OPENPAR":
            expr = parseGroup(tokens)
            break
        case "METHOD":
            expr = parseMethod(token.value, tokens);
            break
        default:
            return [expr, tokens.next().value]
    }
    token = tokens.next().value
    if (!token) return [expr, token]

    if (token.type == "OR"){
        const [right, token] = parseExpression(tokens)
        return [new Or(expr, right), token]
    }
    if (token.type == "AND"){
        const [right, token] = parseExpression(tokens)
        return [new And(expr, right), token]
    }
    throw "Invalid syntax"
}

export function parseTraefikRule(rule) {
    rule = rule.trim()
    const parsers = {
        "METHOD": /(HeadersRegexp|HostHeader|HostRegexp|PathPrefix|Headers|HostSNI|Method|Query|Host|Path)/,
        "OPENPAR": /\(/,
        "CLOSEPAR": /\)/,
        "COMMA": /,/,
        "AND": /&&/,
        "OR": /\|\|/,
        "STRING": /`[^`]+`/,
        "SPACE": /\s+/
    }

    const tokens = tokenizer(rule, parsers)
    const [expr, _] = parseExpression(tokens)
    console.debug(expr)
}

export function isValidRule(rule){
    if (!rule) return true
    try {
        parseTraefikRule(rule)
        return true
    } catch(e){
        return false
    }
}
