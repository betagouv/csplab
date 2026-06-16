import{l as T,a4 as R,f as y,ab as W,A as F,a1 as I,x as j,K as r,h as u,W as g,g as f,e as K,F as U,P as H,j as $,i as J,O as P,a8 as L}from"./vue.esm-bundler-7zVN4DZj.js";import{a as Q,C as X}from"./CspCheckbox-BC9EtbGX.js";import{_ as Y}from"./CspIcon-ClPxlQGO.js";import{_ as Z}from"./_plugin-vue_export-helper-DlAUqK2U.js";import"./useForwardExpose-Owox9Wch.js";import"./nullish-CHIgUVhi.js";import"./isValueEqualOrExist-DvmIGGK4.js";import"./ohash.D__AXeF1-Cq3NGnZa.js";import"./VisuallyHiddenInput-C23Rx6z8.js";import"./usePrimitiveElement-BQYvfrMI.js";import"./VisuallyHidden-BOK6EsXA.js";import"./Primitive-DzgJnGz8.js";import"./RovingFocusItem-CG3LidS2.js";import"./useId-Blg3GNwK.js";import"./RovingFocusGroup-C-W6CSoP.js";import"./ConfigProvider-BVLqxNYe.js";import"./Presence-BoZiCw1w.js";import"./iconify-DRloO12f.js";const ee={key:0,class:"csp-checkbox-group__legend"},ae={class:"csp-checkbox-group__items"},se={key:1,class:"csp-checkbox-group__error",role:"alert"},E=T({__name:"CspCheckboxGroup",props:j({options:{},label:{},name:{},disabled:{type:Boolean,default:!1},size:{default:"md"},error:{type:Boolean,default:!1},errorMessage:{}},{modelValue:{required:!0},modelModifiers:{}}),emits:["update:modelValue"],setup(e){const a=R(e,"modelValue");function s(m){a.value=m.filter(b=>typeof b=="string")}return(m,b)=>(r(),y(I(X),{"model-value":a.value,as:"fieldset",class:F(["csp-checkbox-group",[{"csp-checkbox-group--disabled":e.disabled},{"csp-checkbox-group--error":e.error}]]),name:e.name,disabled:e.disabled,"onUpdate:modelValue":s},{default:W(()=>[e.label?(r(),u("legend",ee,g(e.label),1)):f("",!0),K("div",ae,[(r(!0),u(U,null,H(e.options,o=>(r(),y(Q,{key:o.value,value:o.value,label:o.label,disabled:e.disabled||o.disabled,size:e.size,error:e.error},null,8,["value","label","disabled","size","error"]))),128))]),e.error&&e.errorMessage?(r(),u("p",se,[$(Y,{name:"ri:error-warning-fill",size:14}),J(" "+g(e.errorMessage),1)])):f("",!0)]),_:1},8,["model-value","class","name","disabled"]))}}),p=Z(E,[["__scopeId","data-v-ab9a2d90"]]);E.__docgenInfo={exportName:"default",displayName:"CspCheckboxGroup",type:1,props:[{name:"options",global:!1,description:"",tags:[],required:!0,type:"CspCheckboxGroupOption[]",declarations:[],schema:{kind:"array",type:"CspCheckboxGroupOption[]"}},{name:"label",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"name",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"disabled",global:!1,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]},default:"false"},{name:"size",global:!1,description:"",tags:[],required:!1,type:"CspCheckboxSize",declarations:[],schema:{kind:"array",type:"CspCheckboxSize"},default:'"md"'},{name:"error",global:!1,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]},default:"false"},{name:"errorMessage",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"modelValue",global:!1,description:"",tags:[],required:!0,type:"string[]",declarations:[],schema:{kind:"array",type:"string[]"}},{name:"key",global:!0,description:"",tags:[],required:!1,type:"PropertyKey",declarations:[],schema:{kind:"enum",type:"PropertyKey",schema:["string","number","symbol"]}},{name:"ref",global:!0,description:"",tags:[],required:!1,type:"VNodeRef",declarations:[],schema:{kind:"enum",type:"VNodeRef",schema:["string","Ref<any, any>",{kind:"event",type:"(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void"}]}},{name:"ref_for",global:!0,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"ref_key",global:!0,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"class",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"},{name:"style",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"}],events:[{name:"update:modelValue",description:"",tags:[],type:"[value: string[]]",signature:'(event: "update:modelValue", value: string[]): void',declarations:[],schema:[{kind:"array",type:"string[]"}]}],slots:[],exposed:[{name:"error",type:"boolean",description:"",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"disabled",type:"boolean",description:"",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"size",type:"any",description:"",declarations:[],schema:"any"},{name:"name",type:"string",description:"",declarations:[],schema:"string"},{name:"label",type:"string",description:"",declarations:[],schema:"string"},{name:"errorMessage",type:"string",description:"",declarations:[],schema:"string"},{name:"modelValue",type:"string[]",description:"",declarations:[],schema:{kind:"array",type:"string[]"}},{name:"options",type:"CspCheckboxGroupOption[]",description:"",declarations:[],schema:{kind:"array",type:"CspCheckboxGroupOption[]"}}],sourceFiles:"/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspCheckboxGroup/CspCheckboxGroup.vue"};const re=[{value:"design",label:"Design"},{value:"dev",label:"Développement"},{value:"product",label:"Produit"},{value:"data",label:"Données"}],Ce={title:"Éléments/Génériques/CspCheckboxGroup",component:p,tags:["autodocs"],parameters:{controls:{include:["modelValue","options","label","name","size","disabled","error","errorMessage"]},docs:{description:{component:"Groupe de cases à cocher pour une sélection multiple. Liez le tableau des valeurs sélectionnées via `v-model`. Si aucun `label` visuel n'est rendu, fournissez un nom accessible au fieldset via `aria-label`."}}},argTypes:{modelValue:{control:{type:"object"},description:"Valeurs actuellement cochées.",table:{type:{summary:"string[]"},defaultValue:{summary:"[]"}}},options:{control:{type:"object"},description:"Liste des options disponibles.",table:{type:{summary:"{ value: string; label: string; disabled?: boolean }[]"}}},label:{control:{type:"text"},description:"Légende visible pour le groupe (rendue via une balise `<legend>`).",table:{type:{summary:"string"}}},name:{control:{type:"text"},description:"Nom HTML partagé par les cases à cocher pour une soumission de formulaire native.",table:{type:{summary:"string"}}},disabled:{control:{type:"boolean"},description:"Désactive l'ensemble du groupe.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},size:{control:{type:"radio"},options:["sm","md","lg"],description:"Taille des cases à cocher.",table:{type:{summary:"'sm' | 'md' | 'lg'"},defaultValue:{summary:"'md'"}}},error:{control:{type:"boolean"},description:"Affiche le groupe en état d'erreur.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},errorMessage:{control:{type:"text"},description:"Message d'erreur optionnel, affiché lorsque `error` est actif.",table:{type:{summary:"string"}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{modelValue:["design"],options:re,label:"Domaines",name:"domains",disabled:!1,size:"md",error:!1},render:e=>({components:{CspCheckboxGroup:p},setup(){const a=P(Array.isArray(e.modelValue)?[...e.modelValue]:[]);return L(()=>e.modelValue,s=>{Array.isArray(s)&&(a.value=[...s])}),{args:e,selected:a}},template:`
      <CspCheckboxGroup
        v-bind="args"
        v-model="selected"
      />
    `})},l={},t={args:{options:[{value:"design",label:"Design"},{value:"dev",label:"Développement",disabled:!0},{value:"product",label:"Produit"}],modelValue:["design"]}},n={args:{disabled:!0,modelValue:["design"]}},i={render:e=>({components:{CspCheckboxGroup:p},setup(){const a=P(Array.isArray(e.modelValue)?[...e.modelValue]:[]);return L(()=>e.modelValue,s=>{Array.isArray(s)&&(a.value=[...s])}),{args:e,selected:a}},template:`
      <CspCheckboxGroup
        v-bind="args"
        v-model="selected"
        :label="undefined"
        aria-label="Domaines"
      />
    `})},d={render:()=>({components:{CspCheckboxGroup:p},template:`
      <div style="display: flex; gap: 3rem; align-items: flex-start;">
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">sm</span>
          <CspCheckboxGroup
            :model-value="['a']"
            :options="[{ value: 'a', label: 'Option A' }, { value: 'b', label: 'Option B' }]"
            size="sm"
          />
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">md</span>
          <CspCheckboxGroup
            :model-value="['a']"
            :options="[{ value: 'a', label: 'Option A' }, { value: 'b', label: 'Option B' }]"
            size="md"
          />
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">lg</span>
          <CspCheckboxGroup
            :model-value="['a']"
            :options="[{ value: 'a', label: 'Option A' }, { value: 'b', label: 'Option B' }]"
            size="lg"
          />
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},c={args:{modelValue:[],error:!0,errorMessage:"Veuillez sélectionner au moins une option."}};var v,h,x;l.parameters={...l.parameters,docs:{...(v=l.parameters)==null?void 0:v.docs,source:{originalSource:"{}",...(x=(h=l.parameters)==null?void 0:h.docs)==null?void 0:x.source}}};var k,C,V;t.parameters={...t.parameters,docs:{...(k=t.parameters)==null?void 0:k.docs,source:{originalSource:`{
  args: {
    options: [{
      value: 'design',
      label: 'Design'
    }, {
      value: 'dev',
      label: 'Développement',
      disabled: true
    }, {
      value: 'product',
      label: 'Produit'
    }],
    modelValue: ['design']
  }
}`,...(V=(C=t.parameters)==null?void 0:C.docs)==null?void 0:V.source}}};var z,G,O;n.parameters={...n.parameters,docs:{...(z=n.parameters)==null?void 0:z.docs,source:{originalSource:`{
  args: {
    disabled: true,
    modelValue: ['design']
  }
}`,...(O=(G=n.parameters)==null?void 0:G.docs)==null?void 0:O.source}}};var A,D,q;i.parameters={...i.parameters,docs:{...(A=i.parameters)==null?void 0:A.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspCheckboxGroup
    },
    setup() {
      const selected = ref<string[]>(Array.isArray(args.modelValue) ? [...args.modelValue] : []);
      watch(() => args.modelValue, value => {
        if (Array.isArray(value)) selected.value = [...value];
      });
      return {
        args,
        selected
      };
    },
    template: \`
      <CspCheckboxGroup
        v-bind="args"
        v-model="selected"
        :label="undefined"
        aria-label="Domaines"
      />
    \`
  })
}`,...(q=(D=i.parameters)==null?void 0:D.docs)==null?void 0:q.source}}};var M,B,S;d.parameters={...d.parameters,docs:{...(M=d.parameters)==null?void 0:M.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspCheckboxGroup
    },
    template: \`
      <div style="display: flex; gap: 3rem; align-items: flex-start;">
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">sm</span>
          <CspCheckboxGroup
            :model-value="['a']"
            :options="[{ value: 'a', label: 'Option A' }, { value: 'b', label: 'Option B' }]"
            size="sm"
          />
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">md</span>
          <CspCheckboxGroup
            :model-value="['a']"
            :options="[{ value: 'a', label: 'Option A' }, { value: 'b', label: 'Option B' }]"
            size="md"
          />
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">lg</span>
          <CspCheckboxGroup
            :model-value="['a']"
            :options="[{ value: 'a', label: 'Option A' }, { value: 'b', label: 'Option B' }]"
            size="lg"
          />
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...(S=(B=d.parameters)==null?void 0:B.docs)==null?void 0:S.source}}};var N,_,w;c.parameters={...c.parameters,docs:{...(N=c.parameters)==null?void 0:N.docs,source:{originalSource:`{
  args: {
    modelValue: [],
    error: true,
    errorMessage: 'Veuillez sélectionner au moins une option.'
  }
}`,...(w=(_=c.parameters)==null?void 0:_.docs)==null?void 0:w.source}}};const Ve=["Default","WithDisabledOption","GroupDisabled","NoLabel","Sizes","WithError"];export{l as Default,n as GroupDisabled,i as NoLabel,d as Sizes,t as WithDisabledOption,c as WithError,Ve as __namedExportsOrder,Ce as default};
