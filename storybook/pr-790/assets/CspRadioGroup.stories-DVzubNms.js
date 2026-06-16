import{l as P,a4 as W,f as g,ab as A,A as F,a1 as I,x as T,K as s,h as m,W as f,g as y,e as K,F as j,P as U,j as $,i as H,O as b,a8 as B}from"./vue.esm-bundler-7zVN4DZj.js";import{C as J,R as Q}from"./CspRadio-KZwrHs3C.js";import{_ as X}from"./CspIcon-ClPxlQGO.js";import{_ as Y}from"./_plugin-vue_export-helper-DlAUqK2U.js";import"./useForwardExpose-Owox9Wch.js";import"./RovingFocusItem-CG3LidS2.js";import"./useId-Blg3GNwK.js";import"./Primitive-DzgJnGz8.js";import"./RovingFocusGroup-C-W6CSoP.js";import"./ConfigProvider-BVLqxNYe.js";import"./usePrimitiveElement-BQYvfrMI.js";import"./VisuallyHiddenInput-C23Rx6z8.js";import"./VisuallyHidden-BOK6EsXA.js";import"./handleAndDispatchCustomEvent-ChOKVcqp.js";import"./ohash.D__AXeF1-Cq3NGnZa.js";import"./Presence-BoZiCw1w.js";import"./iconify-DRloO12f.js";const Z={key:0,class:"csp-radio-group__legend"},ee={class:"csp-radio-group__items"},ae={key:1,class:"csp-radio-group__error",role:"alert"},E=P({__name:"CspRadioGroup",props:T({options:{},label:{default:void 0},name:{default:void 0},disabled:{type:Boolean,default:!1},size:{default:"md"},error:{type:Boolean,default:!1},errorMessage:{default:void 0}},{modelValue:{required:!0},modelModifiers:{}}),emits:["update:modelValue"],setup(e){const a=W(e,"modelValue");function o(c){typeof c=="string"&&(a.value=c)}return(c,se)=>(s(),g(I(Q),{"model-value":a.value,as:"fieldset",class:F(["csp-radio-group",{"csp-radio-group--disabled":e.disabled,"csp-radio-group--error":e.error}]),name:e.name,disabled:e.disabled,orientation:"vertical","onUpdate:modelValue":o},{default:A(()=>[e.label?(s(),m("legend",Z,f(e.label),1)):y("",!0),K("div",ee,[(s(!0),m(j,null,U(e.options,r=>(s(),g(J,{key:r.value,value:r.value,label:r.label,disabled:e.disabled||r.disabled,size:e.size,error:e.error},null,8,["value","label","disabled","size","error"]))),128))]),e.error&&e.errorMessage?(s(),m("p",ae,[$(X,{name:"ri:error-warning-fill",size:14}),H(" "+f(e.errorMessage),1)])):y("",!0)]),_:1},8,["model-value","class","name","disabled"]))}}),u=Y(E,[["__scopeId","data-v-8173d66a"]]);E.__docgenInfo={exportName:"default",displayName:"CspRadioGroup",type:1,props:[{name:"options",global:!1,description:"",tags:[],required:!0,type:"CspRadioGroupOption[]",declarations:[],schema:{kind:"array",type:"CspRadioGroupOption[]"}},{name:"label",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string",default:"undefined"},{name:"name",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string",default:"undefined"},{name:"disabled",global:!1,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]},default:"false"},{name:"size",global:!1,description:"",tags:[],required:!1,type:"CspRadioSize",declarations:[],schema:{kind:"array",type:"CspRadioSize"},default:'"md"'},{name:"error",global:!1,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]},default:"false"},{name:"errorMessage",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string",default:"undefined"},{name:"modelValue",global:!1,description:"",tags:[],required:!0,type:"string",declarations:[],schema:"string"},{name:"key",global:!0,description:"",tags:[],required:!1,type:"PropertyKey",declarations:[],schema:{kind:"enum",type:"PropertyKey",schema:["string","number","symbol"]}},{name:"ref",global:!0,description:"",tags:[],required:!1,type:"VNodeRef",declarations:[],schema:{kind:"enum",type:"VNodeRef",schema:["string","Ref<any, any>",{kind:"event",type:"(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void"}]}},{name:"ref_for",global:!0,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"ref_key",global:!0,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"class",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"},{name:"style",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"}],events:[{name:"update:modelValue",description:"",tags:[],type:"[value: string]",signature:'(event: "update:modelValue", value: string): void',declarations:[],schema:["string"]}],slots:[],exposed:[{name:"error",type:"boolean",description:"",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"name",type:"string",description:"",declarations:[],schema:"string"},{name:"disabled",type:"boolean",description:"",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"size",type:"any",description:"",declarations:[],schema:"any"},{name:"label",type:"string",description:"",declarations:[],schema:"string"},{name:"errorMessage",type:"string",description:"",declarations:[],schema:"string"},{name:"modelValue",type:"string",description:"",declarations:[],schema:"string"},{name:"options",type:"CspRadioGroupOption[]",description:"",declarations:[],schema:{kind:"array",type:"CspRadioGroupOption[]"}}],sourceFiles:"/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspRadioGroup/CspRadioGroup.vue"};const oe=[{value:"option-1",label:"Option 1"},{value:"option-2",label:"Option 2"},{value:"option-3",label:"Option 3"}],ze={title:"Éléments/Génériques/CspRadioGroup",component:u,tags:["autodocs"],parameters:{controls:{include:["modelValue","options","label","name","size","disabled","error","errorMessage"]},docs:{description:{component:"Groupe de boutons csp-radio pour une sélection unique exclusive. Liez la valeur sélectionnée via `v-model`. Si aucun `label` visuel n'est rendu, fournissez un nom accessible au fieldset via `aria-label`."}}},argTypes:{modelValue:{control:{type:"text"},description:"Valeur actuellement sélectionnée.",table:{type:{summary:"string"}}},options:{control:{type:"object"},description:"Liste des options disponibles.",table:{type:{summary:"{ value: string; label: string; disabled?: boolean }[]"}}},label:{control:{type:"text"},description:"Légende visible pour le groupe (rendue via une balise `<legend>`).",table:{type:{summary:"string"}}},name:{control:{type:"text"},description:"Attribut `name` partagé pour tous les boutons csp-radio du groupe.",table:{type:{summary:"string"}}},disabled:{control:{type:"boolean"},description:"Désactive l'ensemble du groupe.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},size:{control:{type:"radio"},options:["sm","md","lg"],description:"Libellé du groupe des boutons radio.",table:{type:{summary:"'sm' | 'md' | 'lg'"},defaultValue:{summary:"'md'"}}},error:{control:{type:"boolean"},description:"Affiche le groupe en état d'erreur.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},errorMessage:{control:{type:"text"},description:"Message d'erreur optionnel, affiché lorsque `error` est actif.",table:{type:{summary:"string"}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{modelValue:"option-2",options:oe,label:"Libellé du groupe",name:"size",disabled:!1,size:"md",error:!1},render:e=>({components:{CspRadioGroup:u},setup(){const a=b(e.modelValue??"");return B(()=>e.modelValue,o=>{o!==void 0&&(a.value=o)}),{args:e,selected:a}},template:`
      <CspRadioGroup
        v-bind="args"
        v-model="selected"
      />
    `})},t={},n={args:{options:[{value:"option-1",label:"Option 1"},{value:"option-2",label:"Option 2",disabled:!0},{value:"option-3",label:"Option 3"}],modelValue:"option-1"}},l={args:{disabled:!0,modelValue:"option-2"}},i={render:e=>({components:{CspRadioGroup:u},setup(){const a=b(e.modelValue??"");return B(()=>e.modelValue,o=>{o!==void 0&&(a.value=o)}),{args:e,selected:a}},template:`
      <CspRadioGroup
        v-bind="args"
        v-model="selected"
        :label="undefined"
        aria-label="Libellé du groupe"
      />
    `})},d={render:()=>({components:{CspRadioGroup:u},setup(){const e=["sm","md","lg"],a=b("option-1");return{sizes:e,selected:a}},template:`
      <div class="flex flex-row gap-12">
        <CspRadioGroup
          v-for="size in sizes"
          :key="size"
          v-model="selected"
          :options="[
            { value: 'option-1', label: 'Option 1' },
            { value: 'option-2', label: 'Option 2' },
            { value: 'option-3', label: 'Option 3' },
          ]"
          :size="size"
        />
      </div>
    `})},p={args:{modelValue:"",error:!0,errorMessage:"Veuillez sélectionner une option."}};var v,h,V;t.parameters={...t.parameters,docs:{...(v=t.parameters)==null?void 0:v.docs,source:{originalSource:"{}",...(V=(h=t.parameters)==null?void 0:h.docs)==null?void 0:V.source}}};var z,k,C;n.parameters={...n.parameters,docs:{...(z=n.parameters)==null?void 0:z.docs,source:{originalSource:`{
  args: {
    options: [{
      value: 'option-1',
      label: 'Option 1'
    }, {
      value: 'option-2',
      label: 'Option 2',
      disabled: true
    }, {
      value: 'option-3',
      label: 'Option 3'
    }],
    modelValue: 'option-1'
  }
}`,...(C=(k=n.parameters)==null?void 0:k.docs)==null?void 0:C.source}}};var O,R,G;l.parameters={...l.parameters,docs:{...(O=l.parameters)==null?void 0:O.docs,source:{originalSource:`{
  args: {
    disabled: true,
    modelValue: 'option-2'
  }
}`,...(G=(R=l.parameters)==null?void 0:R.docs)==null?void 0:G.source}}};var q,x,M;i.parameters={...i.parameters,docs:{...(q=i.parameters)==null?void 0:q.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspRadioGroup
    },
    setup() {
      const selected = ref(args.modelValue ?? '');
      watch(() => args.modelValue, value => {
        if (value !== undefined) selected.value = value;
      });
      return {
        args,
        selected
      };
    },
    template: \`
      <CspRadioGroup
        v-bind="args"
        v-model="selected"
        :label="undefined"
        aria-label="Libellé du groupe"
      />
    \`
  })
}`,...(M=(x=i.parameters)==null?void 0:x.docs)==null?void 0:M.source}}};var S,w,L;d.parameters={...d.parameters,docs:{...(S=d.parameters)==null?void 0:S.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspRadioGroup
    },
    setup() {
      const sizes = ['sm', 'md', 'lg'];
      const selected = ref('option-1');
      return {
        sizes,
        selected
      };
    },
    template: \`
      <div class="flex flex-row gap-12">
        <CspRadioGroup
          v-for="size in sizes"
          :key="size"
          v-model="selected"
          :options="[
            { value: 'option-1', label: 'Option 1' },
            { value: 'option-2', label: 'Option 2' },
            { value: 'option-3', label: 'Option 3' },
          ]"
          :size="size"
        />
      </div>
    \`
  })
}`,...(L=(w=d.parameters)==null?void 0:w.docs)==null?void 0:L.source}}};var N,_,D;p.parameters={...p.parameters,docs:{...(N=p.parameters)==null?void 0:N.docs,source:{originalSource:`{
  args: {
    modelValue: '',
    error: true,
    errorMessage: 'Veuillez sélectionner une option.'
  }
}`,...(D=(_=p.parameters)==null?void 0:_.docs)==null?void 0:D.source}}};const ke=["Default","WithDisabledOption","GroupDisabled","NoLabel","Sizes","WithError"];export{t as Default,l as GroupDisabled,i as NoLabel,d as Sizes,n as WithDisabledOption,p as WithError,ke as __namedExportsOrder,ze as default};
