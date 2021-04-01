import gql from "graphql-tag"


function ggql(strings, ...args){
    console.log(args)
    return  String.raw(strings, ...args)
}


const test=  42
const q = ggql`
query test {
    docker {
        dns {
            rules {
                ...rule
            }
        }
    }
}\n
${test}
`




console.log(q)