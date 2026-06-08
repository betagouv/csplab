import{k as P,Z as B,X as $,h as p,Q as u,g,a4 as R,$ as A,e as K,v as L,W as O,j as U,i as W,x as Y,u as Z,H as m,Y as j,K as T,a1 as D}from"./vue.esm-bundler-By9fcp0_.js";import{_ as F}from"./CspIcon-Jm4CDBq2.js";import{_ as G}from"./_plugin-vue_export-helper-DlAUqK2U.js";import"./iconify-CHdUEgWl.js";const H=["for"],Q=["id","name","type","placeholder","disabled","aria-invalid"],X={key:1,class:"csp-input-group__error",role:"alert"},E=P({inheritAttrs:!1,__name:"CspInput",props:Z({type:{default:"text"},placeholder:{},size:{default:"md"},disabled:{type:Boolean,default:!1},error:{type:Boolean,default:!1},errorMessage:{},id:{default:()=>j()},name:{},label:{}},{modelValue:{default:""},modelModifiers:{}}),emits:["update:modelValue"],setup(e){const a=B(e,"modelValue"),s=$();return(r,c)=>(m(),p("div",{class:Y(["csp-input-group",{"csp-input-group--error":e.error}])},[e.label?(m(),p("label",{key:0,class:"csp-input-group__label",for:e.id},u(e.label),9,H)):g("",!0),R(K("input",L(O(s),{id:e.id,"onUpdate:modelValue":c[0]||(c[0]=N=>a.value=N),name:e.name,type:e.type,placeholder:e.placeholder,disabled:e.disabled,"aria-invalid":e.error||void 0,class:["csp-input",[`csp-input--${e.size}`,{"csp-input--error":e.error}]]}),null,16,Q),[[A,a.value]]),e.error&&e.errorMessage?(m(),p("p",X,[U(F,{name:"ri:error-warning-fill",size:14}),W(" "+u(e.errorMessage),1)])):g("",!0)],2))}}),t=G(E,[["__scopeId","data-v-e4fa0a55"]]);E.__docgenInfo={exportName:"default",displayName:"CspInput",type:1,props:[{name:"error",global:!1,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]},default:"false"},{name:"type",global:!1,description:"",tags:[],required:!1,type:'"number" | "search" | "text" | "email" | "password" | "tel" | "url"',declarations:[],schema:{kind:"enum",type:'"number" | "search" | "text" | "email" | "password" | "tel" | "url"',schema:['"number"','"search"','"text"','"email"','"password"','"tel"','"url"']},default:'"text"'},{name:"size",global:!1,description:"",tags:[],required:!1,type:'"md" | "sm" | "lg"',declarations:[],schema:{kind:"enum",type:'"md" | "sm" | "lg"',schema:['"md"','"sm"','"lg"']},default:'"md"'},{name:"disabled",global:!1,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]},default:"false"},{name:"id",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string",default:"useId()"},{name:"name",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"key",global:!0,description:"",tags:[],required:!1,type:"PropertyKey",declarations:[],schema:{kind:"enum",type:"PropertyKey",schema:["string","number","symbol"]}},{name:"ref",global:!0,description:"",tags:[],required:!1,type:"VNodeRef",declarations:[],schema:{kind:"enum",type:"VNodeRef",schema:["string","Ref<any, any>",{kind:"event",type:"(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void"}]}},{name:"ref_for",global:!0,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"ref_key",global:!0,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"class",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"},{name:"style",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"},{name:"label",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"modelValue",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string",default:'""'},{name:"placeholder",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"errorMessage",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"}],events:[{name:"update:modelValue",description:"",tags:[],type:"[value: string]",signature:'(event: "update:modelValue", value: string): void',declarations:[],schema:["string"]}],slots:[],exposed:[{name:"error",type:"boolean",description:"",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"type",type:'"number" | "search" | "text" | "email" | "password" | "tel" | "url"',description:"",declarations:[],schema:{kind:"enum",type:'"number" | "search" | "text" | "email" | "password" | "tel" | "url"',schema:['"number"','"search"','"text"','"email"','"password"','"tel"','"url"']}},{name:"size",type:'"md" | "sm" | "lg"',description:"",declarations:[],schema:{kind:"enum",type:'"md" | "sm" | "lg"',schema:['"md"','"sm"','"lg"']}},{name:"disabled",type:"boolean",description:"",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"id",type:"string",description:"",declarations:[],schema:"string"},{name:"name",type:"string",description:"",declarations:[],schema:"string"},{name:"label",type:"string",description:"",declarations:[],schema:"string"},{name:"modelValue",type:"string",description:"",declarations:[],schema:"string"},{name:"placeholder",type:"string",description:"",declarations:[],schema:"string"},{name:"errorMessage",type:"string",description:"",declarations:[],schema:"string"}],sourceFiles:"/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspInput/CspInput.vue"};const re={title:"Éléments/Génériques/CspInput",component:t,tags:["autodocs"],parameters:{controls:{include:["modelValue","type","placeholder","size","disabled","error","errorMessage","id","name","label"]},docs:{description:{component:"Champ de saisie de texte."}}},argTypes:{modelValue:{control:{type:"text"},description:"Valeur actuelle (v-model).",table:{type:{summary:"string"}}},type:{control:{type:"radio"},options:["text","email","password","search","tel","url","number"],description:"Type d'entrée natif.",table:{type:{summary:"text | email | password | search | tel | url | number"},defaultValue:{summary:"text"}}},placeholder:{control:{type:"text"},description:"Texte d'espace réservé (placeholder).",table:{type:{summary:"string"}}},size:{control:{type:"radio"},options:["sm","md","lg"],description:"Taille de l'entrée.",table:{type:{summary:"sm | md | lg"},defaultValue:{summary:"md"}}},disabled:{control:{type:"boolean"},description:"Désactive l'entrée.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},error:{control:{type:"boolean"},description:"Affiche le champ en état d'erreur.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},errorMessage:{control:{type:"text"},description:"Message d'erreur optionnel, affiché lorsque `error` est actif.",table:{type:{summary:"string"}}},id:{control:{type:"text"},description:"ID optionnel pour l'association du label.",table:{type:{summary:"string"}}},name:{control:{type:"text"},description:"Nom optionnel pour la soumission du formulaire.",table:{type:{summary:"string"}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{modelValue:"",type:"text",placeholder:"Saisir un texte",size:"md",disabled:!1,id:"base-input-story",name:"base-input"},render:e=>({components:{CspInput:t},setup(){const a=T(e.modelValue??"");D(()=>e.modelValue,r=>{a.value=r??""});function s(r){a.value=r}return{args:e,value:a,handleUpdate:s}},template:`
      <div class="w-96">
        <label
          class="block mb-2 text-sm font-medium"
          :for="args.id"
        >
          Libellé
        </label>
        <CspInput
          v-bind="args"
          :model-value="value"
          @update:model-value="handleUpdate"
        />
      </div>
    `})},J=["sm","md","lg"],_=["text","email","password","search","tel","url","number"],l={},n={args:{disabled:!0,modelValue:"Valeur non modifiable"}},o={render:e=>({components:{CspInput:t},setup(){return{sizes:J,args:e}},template:`
      <div class="flex flex-col gap-6">
        <div
          v-for="s in sizes"
          :key="s"
          class="w-96"
        >
          <p class="mb-2">{{ s }}</p>
          <CspInput
            v-bind="args"
            :size="s"
            :model-value="'Texte'"
          />
        </div>
      </div>
    `})},i={render:e=>({components:{CspInput:t},setup(){return{types:_,args:e}},template:`
      <div class="flex flex-col gap-6">
        <div
          v-for="t in types"
          :key="t"
          class="w-96"
        >
          <p class="mb-2">{{ t }}</p>
          <CspInput
            v-bind="args"
            :type="t"
            :model-value="t === 'password' ? 'secret' : 'Texte'"
          />
        </div>
      </div>
    `})},d={args:{label:"Libellé input",error:!0,errorMessage:"Ce champ est obligatoire.",modelValue:""},render:e=>({components:{CspInput:t},setup(){const a=T(e.modelValue??"");return D(()=>e.modelValue,s=>{a.value=s??""}),{args:e,value:a}},template:`
      <div class="w-96">
        <CspInput
          v-bind="args"
          :model-value="value"
          @update:model-value="value = $event"
        />
      </div>
    `})};var y,f,b;l.parameters={...l.parameters,docs:{...(y=l.parameters)==null?void 0:y.docs,source:{originalSource:"{}",...(b=(f=l.parameters)==null?void 0:f.docs)==null?void 0:b.source}}};var v,h,x;n.parameters={...n.parameters,docs:{...(v=n.parameters)==null?void 0:v.docs,source:{originalSource:`{
  args: {
    disabled: true,
    modelValue: 'Valeur non modifiable'
  }
}`,...(x=(h=n.parameters)==null?void 0:h.docs)==null?void 0:x.source}}};var V,k,w;o.parameters={...o.parameters,docs:{...(V=o.parameters)==null?void 0:V.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspInput
    },
    setup() {
      return {
        sizes: SIZES,
        args
      };
    },
    template: \`
      <div class="flex flex-col gap-6">
        <div
          v-for="s in sizes"
          :key="s"
          class="w-96"
        >
          <p class="mb-2">{{ s }}</p>
          <CspInput
            v-bind="args"
            :size="s"
            :model-value="'Texte'"
          />
        </div>
      </div>
    \`
  })
}`,...(w=(k=o.parameters)==null?void 0:k.docs)==null?void 0:w.source}}};var C,I,q;i.parameters={...i.parameters,docs:{...(C=i.parameters)==null?void 0:C.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspInput
    },
    setup() {
      return {
        types: TYPES,
        args
      };
    },
    template: \`
      <div class="flex flex-col gap-6">
        <div
          v-for="t in types"
          :key="t"
          class="w-96"
        >
          <p class="mb-2">{{ t }}</p>
          <CspInput
            v-bind="args"
            :type="t"
            :model-value="t === 'password' ? 'secret' : 'Texte'"
          />
        </div>
      </div>
    \`
  })
}`,...(q=(I=i.parameters)==null?void 0:I.docs)==null?void 0:q.source}}};var z,S,M;d.parameters={...d.parameters,docs:{...(z=d.parameters)==null?void 0:z.docs,source:{originalSource:`{
  args: {
    label: 'Libellé input',
    error: true,
    errorMessage: 'Ce champ est obligatoire.',
    modelValue: ''
  },
  render: (args: CspInputProps) => ({
    components: {
      CspInput
    },
    setup() {
      const value = ref(args.modelValue ?? '');
      watch(() => args.modelValue, nextValue => {
        value.value = nextValue ?? '';
      });
      return {
        args,
        value
      };
    },
    template: \`
      <div class="w-96">
        <CspInput
          v-bind="args"
          :model-value="value"
          @update:model-value="value = $event"
        />
      </div>
    \`
  })
}`,...(M=(S=d.parameters)==null?void 0:S.docs)==null?void 0:M.source}}};const le=["Default","Disabled","Sizes","Types","WithError"];export{l as Default,n as Disabled,o as Sizes,i as Types,d as WithError,le as __namedExportsOrder,re as default};
