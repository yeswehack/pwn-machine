import re
import json
import textwrap


def uncamel(s):
    space = lambda g: " " + g.group(0)
    return re.sub("(?<!^)[A-Z][a-z]", space, s).capitalize()


def generate_bool(name):
    return f"""<q-toggle label="{uncamel(name)}" v-model="form.{name}" />"""


def generate_number(name):
    return f"""<q-input type="number" label="{uncamel(name)}" v-model.number="form.{name}" />"""


def generate_string(name):
    return f"""<q-input label="{uncamel(name)}" v-model="form.{name}" />"""


def generate_list(name):
    return f"""<list-input label="{uncamel(name)}" v-model="form.{name}" />"""


def generate_component(name):
    return f"""<component :is="formChildren.{name}" label="{uncamel(name)}" v-model="form.{name}" />"""


def fake_json(dict):
    out = "{\n"
    for name, value in dict.items():
        out += f"  {name}: "
        if value in ["String", "Boolean", "Int"]:
            out += "null"
        elif value in ["[String]"]:
            out += "[]"
        elif value == "KV":
            out += "HeadersInput"
        else:
            out += name
        out += ",\n"
    out += "}"
    return out


base_tpl = """
<template>
  <div class="column q-gutter-md">
  <div class="text-h6" v-if="!hideTitle">{LABEL}</div>
{HTML}
  </div>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
{IMPORTS}
export default {{
    props: {{
        hideTitle: {{type: Boolean, default: false}}
    }},
    components: {{ {COMPONENTS} }},
    mixins: [DeepForm],
    formDefinition: {FORM_DEF},
}}
</script>
"""

sub_tpl = """
<template>
  <q-list separator class="rounded-borders" bordered>
    <q-expansion-item expand-separator icon="label" label="{LABEL}">
      <q-separator />
      <q-card>
        <q-card-section>
        <div class="column q-gutter-sm">
{HTML}
</div>
        </q-card-section>
        <q-card-section v-if="0">
          <pre>{{{{form}}}}</pre>
        </q-card-section>
      </q-card>
    </q-expansion-item>
  </q-list>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
{IMPORTS}
export default {{
    components: {{ {COMPONENTS} }},
    mixins: [DeepForm],
    formDefinition: {FORM_DEF},
}}
</script>
"""

def generate_vue_form_for_type(name, definition, depth=0):
    print(name, depth)
    if depth == 0:
        tpl = base_tpl
    else:
        tpl = sub_tpl
    form_def = fake_json(definition)

    imports = set()
    components = set()
    html = []
    for child_name, child_type in definition.items():
        if isinstance(child_type, dict):
            print(name, child_name)
            generate_vue_form_for_type(child_name, child_type, depth+1)
            imports.add(f"import {child_name} from './{child_name}.vue';")
            components.add(child_name)
            html.append(generate_component(child_name))

        elif child_type == "Boolean":
            html.append(generate_bool(child_name))
        elif child_type == "Int":
            html.append(generate_number(child_name))
        elif child_type == "String":
            html.append(generate_string(child_name))
        elif child_type == "[String]":
            imports.add("import ListInput from 'src/components/ListInput.vue';")
            components.add("ListInput")
            html.append(generate_list(child_name))
        elif child_type == "KV":
            imports.add("import HeadersInput from 'src/components/Traefik/HeadersInput.vue';")
            components.add("HeadersInput")
            html.append(generate_component(child_name))
        else:
            raise NotImplementedError(f"CANNOT HANDLE {child_name} {child_type}")
    full_html = textwrap.indent("\n".join(html), " " * 6)

    vue = tpl.format(
        LABEL=uncamel(name),
        HTML=full_html,
        FORM_DEF=form_def,
        IMPORTS=textwrap.indent("\n".join(imports), " "),
        COMPONENTS=textwrap.indent(", ".join(components), " "),
    )
    with open(f"{path}/{name}.vue", "w") as f:
        f.write(vue)



path = "/home/bitk/ywh/git/pwnmachinev2/dockers/manager/front/src/components/Traefik/Middleware/Forms"


def generate_vue_from_types(types):
    index = ""
    for name, definition in list(types.items()):
        generate_vue_form_for_type(name, definition)
        index += f'import {name} from "./{name}.vue"\n'
    index += "export default { " + ",\n".join(types) + "}"
    with open(f"{path}/index.js", "w") as f:
        f.write(index)