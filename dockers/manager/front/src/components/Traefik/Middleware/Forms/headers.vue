
<template>
  <div class="column q-gutter-md">
  <div class="text-h6" v-if="!hideTitle">Headers</div>
      <q-toggle label="Access control allow credentials" v-model="form.accessControlAllowCredentials" />
      <list-input label="Access control allow headers" v-model="form.accessControlAllowHeaders" />
      <list-input label="Access control allow methods" v-model="form.accessControlAllowMethods" />
      <q-input label="Access control allow origin" v-model="form.accessControlAllowOrigin" />
      <list-input label="Access control allow origin list" v-model="form.accessControlAllowOriginList" />
      <list-input label="Access control allow origin list regex" v-model="form.accessControlAllowOriginListRegex" />
      <list-input label="Access control expose headers" v-model="form.accessControlExposeHeaders" />
      <q-input type="number" label="Access control max age" v-model.number="form.accessControlMaxAge" />
      <q-toggle label="Add vary header" v-model="form.addVaryHeader" />
      <list-input label="Allowed hosts" v-model="form.allowedHosts" />
      <q-toggle label="Browser xss filter" v-model="form.browserXssFilter" />
      <q-input label="Content security policy" v-model="form.contentSecurityPolicy" />
      <q-toggle label="Content type nosniff" v-model="form.contentTypeNosniff" />
      <q-input label="Custom browserxss value" v-model="form.customBrowserXSSValue" />
      <q-input label="Custom frame options value" v-model="form.customFrameOptionsValue" />
      <component :is="formChildren.customRequestHeaders" label="Custom request headers" v-model="form.customRequestHeaders" />
      <component :is="formChildren.customResponseHeaders" label="Custom response headers" v-model="form.customResponseHeaders" />
      <q-input label="Feature policy" v-model="form.featurePolicy" />
      <q-toggle label="Forcests header" v-model="form.forceSTSHeader" />
      <q-toggle label="Frame deny" v-model="form.frameDeny" />
      <list-input label="Hosts proxy headers" v-model="form.hostsProxyHeaders" />
      <q-toggle label="Is development" v-model="form.isDevelopment" />
      <q-input label="Public key" v-model="form.publicKey" />
      <q-input label="Referrer policy" v-model="form.referrerPolicy" />
      <q-toggle label="Ssl force host" v-model="form.sslForceHost" />
      <q-input label="Ssl host" v-model="form.sslHost" />
      <component :is="formChildren.sslProxyHeaders" label="Ssl proxy headers" v-model="form.sslProxyHeaders" />
      <q-toggle label="Ssl redirect" v-model="form.sslRedirect" />
      <q-toggle label="Ssl temporary redirect" v-model="form.sslTemporaryRedirect" />
      <q-toggle label="Sts include subdomains" v-model="form.stsIncludeSubdomains" />
      <q-toggle label="Sts preload" v-model="form.stsPreload" />
      <q-input type="number" label="Sts seconds" v-model.number="form.stsSeconds" />
  </div>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
 import ListInput from 'src/components/ListInput.vue';
 import HeadersInput from 'src/components/Traefik/HeadersInput.vue';

export default {
    props: {
        hideTitle: {type: Boolean, default: false}
    },
    components: {  ListInput, HeadersInput },
    mixins: [DeepForm],
    formDefinition: {
  accessControlAllowCredentials: null,
  accessControlAllowHeaders: [],
  accessControlAllowMethods: [],
  accessControlAllowOrigin: null,
  accessControlAllowOriginList: [],
  accessControlAllowOriginListRegex: [],
  accessControlExposeHeaders: [],
  accessControlMaxAge: null,
  addVaryHeader: null,
  allowedHosts: [],
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
  hostsProxyHeaders: [],
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
