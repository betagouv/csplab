import{k as D,Z as N,X as P,H as c,h as m,Q as u,g,a4 as B,a0 as A,e as U,v as $,W as K,j as O,i as W,x as Z,u as L,Y as X,K as E,a1 as S}from"./vue.esm-bundler-By9fcp0_.js";import{_ as j}from"./CspIcon-Jm4CDBq2.js";import{_ as F}from"./_plugin-vue_export-helper-DlAUqK2U.js";import"./iconify-CHdUEgWl.js";const G=["for"],H=["id","placeholder","rows","disabled","aria-invalid"],Q={key:1,class:"csp-textarea-group__error",role:"alert"},I=D({inheritAttrs:!1,__name:"CspTextarea",props:L({placeholder:{},rows:{default:4},disabled:{type:Boolean,default:!1},error:{type:Boolean,default:!1},errorMessage:{},resize:{default:"vertical"},id:{default:()=>X()},label:{default:void 0}},{modelValue:{default:""},modelModifiers:{}}),emits:["update:modelValue"],setup(e){const a=e,r=N(e,"modelValue"),t=P();return(ee,p)=>(c(),m("div",{class:Z(["csp-textarea-group",{"csp-textarea-group--error":e.error}])},[e.label?(c(),m("label",{key:0,class:"csp-textarea-group__label",for:e.id},u(e.label),9,G)):g("",!0),B(U("textarea",$(K(t),{id:e.id,"onUpdate:modelValue":p[0]||(p[0]=_=>r.value=_),class:["csp-textarea",[`csp-textarea--resize-${a.resize}`,{"csp-textarea--error":a.error}]],placeholder:a.placeholder,rows:a.rows,disabled:a.disabled,"aria-invalid":e.error||void 0}),null,16,H),[[A,r.value]]),e.error&&e.errorMessage?(c(),m("p",Q,[O(j,{name:"ri:error-warning-fill",size:14}),W(" "+u(e.errorMessage),1)])):g("",!0)],2))}}),s=F(I,[["__scopeId","data-v-35dd6122"]]);I.__docgenInfo={exportName:"default",displayName:"CspTextarea",type:1,props:[{name:"error",global:!1,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]},default:"false"},{name:"resize",global:!1,description:"",tags:[],required:!1,type:'"vertical" | "none" | "horizontal" | "both"',declarations:[],schema:{kind:"enum",type:'"vertical" | "none" | "horizontal" | "both"',schema:['"vertical"','"none"','"horizontal"','"both"']},default:'"vertical"'},{name:"label",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string",default:"undefined"},{name:"disabled",global:!1,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]},default:"false"},{name:"id",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string",default:"useId()"},{name:"rows",global:!1,description:"",tags:[],required:!1,type:"number",declarations:[],schema:"number",default:"4"},{name:"key",global:!0,description:"",tags:[],required:!1,type:"PropertyKey",declarations:[],schema:{kind:"enum",type:"PropertyKey",schema:["string","number","symbol"]}},{name:"ref",global:!0,description:"",tags:[],required:!1,type:"VNodeRef",declarations:[],schema:{kind:"enum",type:"VNodeRef",schema:["string","Ref<any, any>",{kind:"event",type:"(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void"}]}},{name:"ref_for",global:!0,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"ref_key",global:!0,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"class",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"},{name:"style",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"},{name:"placeholder",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"errorMessage",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"modelValue",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string",default:'""'}],events:[{name:"update:modelValue",description:"",tags:[],type:"[value: string]",signature:'(event: "update:modelValue", value: string): void',declarations:[],schema:["string"]}],slots:[],exposed:[{name:"error",type:"boolean",description:"",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"resize",type:'"vertical" | "none" | "horizontal" | "both"',description:"",declarations:[],schema:{kind:"enum",type:'"vertical" | "none" | "horizontal" | "both"',schema:['"vertical"','"none"','"horizontal"','"both"']}},{name:"label",type:"string",description:"",declarations:[],schema:"string"},{name:"disabled",type:"boolean",description:"",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"id",type:"string",description:"",declarations:[],schema:"string"},{name:"rows",type:"number",description:"",declarations:[],schema:"number"},{name:"placeholder",type:"string",description:"",declarations:[],schema:"string"},{name:"errorMessage",type:"string",description:"",declarations:[],schema:"string"},{name:"modelValue",type:"string",description:"",declarations:[],schema:"string"}],sourceFiles:"/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspTextarea/CspTextarea.vue"};const Y="base-textarea-story",ne={title:"Éléments/Génériques/CspTextarea",component:s,tags:["autodocs"],parameters:{controls:{include:["modelValue","placeholder","rows","disabled","error","errorMessage","resize","label"]},docs:{description:{component:"Primitive de zone de texte générique, contrôlée via `v-model` (`modelValue` / `update:modelValue`)."}}},argTypes:{modelValue:{control:{type:"text"},description:"Valeur actuelle de la zone de texte (v-model).",table:{type:{summary:"string"}}},placeholder:{control:{type:"text"},description:"Espace réservé natif affiché lorsque le champ est vide.",table:{type:{summary:"string"}}},rows:{control:{type:"number",min:1,max:20},description:"Nombre de lignes visibles.",table:{type:{summary:"number"},defaultValue:{summary:"4"}}},disabled:{control:{type:"boolean"},description:"Désactive la saisie de l'utilisateur.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},error:{control:{type:"boolean"},description:"Affiche le champ en état d'erreur.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},errorMessage:{control:{type:"text"},description:"Message d'erreur optionnel, affiché lorsque `error` est actif.",table:{type:{summary:"string"}}},resize:{control:{type:"radio"},options:["none","vertical","horizontal","both"],description:"Comportement de redimensionnement natif.",table:{type:{summary:"none | vertical | horizontal | both"},defaultValue:{summary:"vertical"}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{modelValue:"",placeholder:"Tapez votre message…",rows:4,disabled:!1,resize:"vertical"},render:e=>({components:{CspTextarea:s},setup(){const a=E(e.modelValue??"");S(()=>e.modelValue,t=>{a.value=t??""});function r(t){a.value=t}return{args:e,value:a,onUpdate:r,textareaId:Y}},template:`
      <div class="w-96">
        <label
          :for="textareaId"
          class="block mb-2 text-sm font-medium"
        >
          Message
        </label>
        <CspTextarea
          v-bind="args"
          :id="textareaId"
          :model-value="value"
          @update:model-value="onUpdate"
        />
      </div>
    `})},J=["none","vertical","horizontal","both"],n={},o={render:e=>({components:{CspTextarea:s},setup(){return{args:e}},template:`
      <div class="flex flex-col gap-8 max-w-xl">
        <div>
          <p class="mb-2">Par défaut</p>
          <CspTextarea v-bind="args" placeholder="Tapez votre message…" />
        </div>
        <div>
          <p class="mb-2">Désactivé</p>
          <CspTextarea v-bind="args" :disabled="true" placeholder="Désactivé" />
        </div>
      </div>
    `})},l={render:e=>({components:{CspTextarea:s},setup(){return{args:e,resizes:J}},template:`
      <div class="flex flex-col gap-8 max-w-xl">
        <div
          v-for="r in resizes"
          :key="r"
        >
          <p class="mb-2">Redimensionnement : {{ r }}</p>
          <CspTextarea
            v-bind="args"
            :resize="r"
            :rows="3"
            :modelValue="'Un texte sur\\nplusieurs lignes.'"
          />
        </div>
      </div>
    `})},i={render:e=>({components:{CspTextarea:s},setup(){return{args:e,rowsVariants:[2,4,8]}},template:`
      <div class="flex flex-col gap-8 max-w-xl">
        <div
          v-for="r in rowsVariants"
          :key="r"
        >
          <p class="mb-2">Lignes (rows) : {{ r }}</p>
          <CspTextarea
            v-bind="args"
            :rows="r"
            :modelValue="'Contenu de démonstration'"
          />
        </div>
      </div>
    `})},d={args:{label:"Message",error:!0,errorMessage:"Ce champ est obligatoire.",placeholder:"Tapez votre message…",modelValue:""},render:e=>({components:{CspTextarea:s},setup(){const a=E(e.modelValue??"");return S(()=>e.modelValue,r=>{a.value=r??""}),{args:e,value:a}},template:`
      <div class="max-w-xl">
        <CspTextarea
          v-bind="args"
          :model-value="value"
          @update:model-value="value = $event"
        />
      </div>
    `})};var f,v,b;n.parameters={...n.parameters,docs:{...(f=n.parameters)==null?void 0:f.docs,source:{originalSource:"{}",...(b=(v=n.parameters)==null?void 0:v.docs)==null?void 0:b.source}}};var y,h,x;o.parameters={...o.parameters,docs:{...(y=o.parameters)==null?void 0:y.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspTextarea
    },
    setup() {
      return {
        args
      };
    },
    template: \`
      <div class="flex flex-col gap-8 max-w-xl">
        <div>
          <p class="mb-2">Par défaut</p>
          <CspTextarea v-bind="args" placeholder="Tapez votre message…" />
        </div>
        <div>
          <p class="mb-2">Désactivé</p>
          <CspTextarea v-bind="args" :disabled="true" placeholder="Désactivé" />
        </div>
      </div>
    \`
  })
}`,...(x=(h=o.parameters)==null?void 0:h.docs)==null?void 0:x.source}}};var V,w,z;l.parameters={...l.parameters,docs:{...(V=l.parameters)==null?void 0:V.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspTextarea
    },
    setup() {
      return {
        args,
        resizes: RESIZES
      };
    },
    template: \`
      <div class="flex flex-col gap-8 max-w-xl">
        <div
          v-for="r in resizes"
          :key="r"
        >
          <p class="mb-2">Redimensionnement : {{ r }}</p>
          <CspTextarea
            v-bind="args"
            :resize="r"
            :rows="3"
            :modelValue="'Un texte sur\\\\nplusieurs lignes.'"
          />
        </div>
      </div>
    \`
  })
}`,...(z=(w=l.parameters)==null?void 0:w.docs)==null?void 0:z.source}}};var C,T,k;i.parameters={...i.parameters,docs:{...(C=i.parameters)==null?void 0:C.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspTextarea
    },
    setup() {
      const rowsVariants = [2, 4, 8] as const;
      return {
        args,
        rowsVariants
      };
    },
    template: \`
      <div class="flex flex-col gap-8 max-w-xl">
        <div
          v-for="r in rowsVariants"
          :key="r"
        >
          <p class="mb-2">Lignes (rows) : {{ r }}</p>
          <CspTextarea
            v-bind="args"
            :rows="r"
            :modelValue="'Contenu de démonstration'"
          />
        </div>
      </div>
    \`
  })
}`,...(k=(T=i.parameters)==null?void 0:T.docs)==null?void 0:k.source}}};var q,M,R;d.parameters={...d.parameters,docs:{...(q=d.parameters)==null?void 0:q.docs,source:{originalSource:`{
  args: {
    label: 'Message',
    error: true,
    errorMessage: 'Ce champ est obligatoire.',
    placeholder: 'Tapez votre message…',
    modelValue: ''
  },
  render: (args: CspTextareaProps) => ({
    components: {
      CspTextarea
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
      <div class="max-w-xl">
        <CspTextarea
          v-bind="args"
          :model-value="value"
          @update:model-value="value = $event"
        />
      </div>
    \`
  })
}`,...(R=(M=d.parameters)==null?void 0:M.docs)==null?void 0:R.source}}};const oe=["Default","States","Resizes","Rows","WithError"];export{n as Default,l as Resizes,i as Rows,o as States,d as WithError,oe as __namedExportsOrder,ne as default};
