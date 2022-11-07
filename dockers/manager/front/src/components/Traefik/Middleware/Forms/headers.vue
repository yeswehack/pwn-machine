
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">Headers</div>
      <q-toggle v-model="form.accessControlAllowCredentials" label="Access control allow credentials" />
      <component :is="formChildren.accessControlAllowHeaders" v-model="form.accessControlAllowHeaders" label="Access control allow headers" />
      <component :is="formChildren.accessControlAllowMethods" v-model="form.accessControlAllowMethods" label="Access control allow methods" />
      <q-input v-model="form.accessControlAllowOrigin" label="Access control allow origin" />
      <component :is="formChildren.accessControlAllowOriginList" v-model="form.accessControlAllowOriginList" label="Access control allow origin list" />
      <component :is="formChildren.accessControlAllowOriginListRegex" v-model="form.accessControlAllowOriginListRegex" label="Access control allow origin list regex" />
      <component :is="formChildren.accessControlExposeHeaders" v-model="form.accessControlExposeHeaders" label="Access control expose headers" />
      <q-input v-model.number="form.accessControlMaxAge" type="number" label="Access control max age" />
      <q-toggle v-model="form.addVaryHeader" label="Add vary header" />
      <component :is="formChildren.allowedHosts" v-model="form.allowedHosts" label="Allowed hosts" />
      <q-toggle v-model="form.browserXssFilter" label="Browser xss filter" />
      <q-input v-model="form.contentSecurityPolicy" label="Content security policy" />
      <q-toggle v-model="form.contentTypeNosniff" label="Content type nosniff" />
      <q-input v-model="form.customBrowserXSSValue" label="Custom browserxss value" />
      <q-input v-model="form.customFrameOptionsValue" label="Custom frame options value" />
      <component :is="formChildren.customRequestHeaders" v-model="form.customRequestHeaders" label="Custom request headers" />
      <component :is="formChildren.customResponseHeaders" v-model="form.customResponseHeaders" label="Custom response headers" />
      <q-input v-model="form.featurePolicy" label="Feature policy" />
      <q-toggle v-model="form.forceSTSHeader" label="Forcests header" />
      <q-toggle v-model="form.frameDeny" label="Frame deny" />
      <component :is="formChildren.hostsProxyHeaders" v-model="form.hostsProxyHeaders" label="Hosts proxy headers" />
      <q-toggle v-model="form.isDevelopment" label="Is development" />
      <q-input v-model="form.publicKey" label="Public key" />
      <q-input v-model="form.referrerPolicy" label="Referrer policy" />
      <q-toggle v-model="form.sslForceHost" label="Ssl force host" />
      <q-input v-model="form.sslHost" label="Ssl host" />
      <component :is="formChildren.sslProxyHeaders" v-model="form.sslProxyHeaders" label="Ssl proxy headers" />
      <q-toggle v-model="form.sslRedirect" label="Ssl redirect" />
      <q-toggle v-model="form.sslTemporaryRedirect" label="Ssl temporary redirect" />
      <q-toggle v-model="form.stsIncludeSubdomains" label="Sts include subdomains" />
      <q-toggle v-model="form.stsPreload" label="Sts preload" />
      <q-input v-model.number="form.stsSeconds" type="number" label="Sts seconds" />
  </div>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
import HeadersInput from 'src/components/Traefik/HeadersInput.vue';
import StringListInput from 'src/components/StringListInput.vue';
export default {
    components: {  HeadersInput },
    mixins: [DeepForm],
    props: {
        hideTitle: {type: Boolean, default: false}
    },
    formDefinition: {
  accessControlAllowCredentials: null,
  accessControlAllowHeaders: StringListInput,
  accessControlAllowMethods: StringListInput,
  accessControlAllowOrigin: null,
  accessControlAllowOriginList: StringListInput,
  accessControlAllowOriginListRegex: StringListInput,
  accessControlExposeHeaders: StringListInput,
  accessControlMaxAge: null,
  addVaryHeader: null,
  allowedHosts: StringListInput,
  browserXssFilter: null,
  contentSecurityPolicy: null,
  contentTypeNosniff: null,
  customBrowserXSSValue: null,
  customFrameOptionsValue: null,
  customRequestHeaders: HeadersInput,
  customResponseHeaders: HeadersInput,
  featurePolicy: null,
  forceSTSHeader: null,
  frameDeny: null,
  hostsProxyHeaders: StringListInput,
  isDevelopment: null,
  publicKey: null,
  referrerPolicy: null,
  sslForceHost: null,
  sslHost: null,
  sslProxyHeaders: HeadersInput,
  sslRedirect: null,
  sslTemporaryRedirect: null,
  stsIncludeSubdomains: null,
  stsPreload: null,
  stsSeconds: null,
},
}
</script>
