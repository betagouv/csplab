import{l as g,_ as F,K as p,f as b,ab as v,Q as D,a1 as s,g as L,y as W,ad as j,ae as G,b as V,a4 as H,h as Q,j as k,e as U,W as J,A as X,x as Y,a3 as Z,O as m,a8 as ee}from"./vue.esm-bundler-7zVN4DZj.js";import{q as ae,l as I,a as te}from"./useForwardExpose-qwf_wVRM.js";import{u as se}from"./useFormControl-5LFzebFo.js";import{P as K}from"./Primitive-DzgJnGz8.js";import{V as le}from"./VisuallyHiddenInput-CPKKsE9z.js";import{_ as re}from"./_plugin-vue_export-helper-DlAUqK2U.js";import"./usePrimitiveElement-BQ6g5-es.js";import"./VisuallyHidden-BOK6EsXA.js";const[oe,ne]=te("SwitchRoot");var ie=g({__name:"SwitchRoot",props:{defaultValue:{type:null,required:!1},modelValue:{type:null,required:!1,default:void 0},disabled:{type:Boolean,required:!1},id:{type:String,required:!1},value:{type:String,required:!1,default:"on"},trueValue:{type:null,required:!1,default:()=>!0},falseValue:{type:null,required:!1,default:()=>!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:"button"},name:{type:String,required:!1},required:{type:Boolean,required:!1}},emits:["update:modelValue"],setup(a,{emit:l}){const e=a,n=l,{disabled:r}=F(e),f=ae(e,"modelValue",n,{defaultValue:e.defaultValue??e.falseValue,passive:e.modelValue===void 0}),o=V(()=>f.value===e.trueValue);function y(){r.value||(f.value=o.value?e.falseValue:e.trueValue)}const{forwardRef:$,currentElement:w}=I(),M=se(w),A=V(()=>{var t;return e.id&&w.value?(t=document.querySelector(`[for="${e.id}"]`))==null?void 0:t.innerText:void 0});return ne({checked:o,toggleCheck:y,disabled:r}),(t,pe)=>(p(),b(s(K),W(t.$attrs,{id:t.id,ref:s($),role:"switch",type:t.as==="button"?"button":void 0,value:t.value,"aria-label":t.$attrs["aria-label"]||A.value,"aria-checked":o.value,"aria-required":t.required,"data-state":o.value?"checked":"unchecked","data-disabled":s(r)?"":void 0,"as-child":t.asChild,as:t.as,disabled:s(r),onClick:y,onKeydown:j(G(y,["prevent"]),["enter"])}),{default:v(()=>[D(t.$slots,"default",{modelValue:s(f),checked:o.value}),s(M)&&t.name?(p(),b(s(le),{key:0,type:"checkbox",name:t.name,disabled:s(r),required:t.required,value:t.value,checked:o.value},null,8,["name","disabled","required","value","checked"])):L("v-if",!0)]),_:3},16,["id","type","value","aria-label","aria-checked","aria-required","data-state","data-disabled","as-child","as","disabled","onKeydown"]))}}),de=ie,ue=g({__name:"SwitchThumb",props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:"span"}},setup(a){const l=oe();return I(),(e,n)=>(p(),b(s(K),{"data-state":s(l).checked.value?"checked":"unchecked","data-disabled":s(l).disabled.value?"":void 0,"as-child":e.asChild,as:e.as},{default:v(()=>[D(e.$slots,"default")]),_:3},8,["data-state","data-disabled","as-child","as"]))}}),ce=ue;const me={class:"csp-switch__label"},T=g({__name:"CspSwitch",props:Y({label:{},disabled:{type:Boolean,default:!1},name:{},id:{default:()=>Z()},size:{default:"md"},error:{type:Boolean,default:!1}},{modelValue:{type:Boolean,required:!0},modelModifiers:{}}),emits:["update:modelValue"],setup(a){const l=H(a,"modelValue");return(e,n)=>(p(),Q("label",{class:X(["csp-switch",[`csp-switch--${a.size}`,{"csp-switch--disabled":a.disabled},{"csp-switch--error":a.error}]])},[k(s(de),{id:a.id,modelValue:l.value,"onUpdate:modelValue":n[0]||(n[0]=r=>l.value=r),class:"csp-switch__root",disabled:a.disabled,name:a.name},{default:v(()=>[k(s(ce),{class:"csp-switch__thumb"})]),_:1},8,["id","modelValue","disabled","name"]),U("span",me,J(a.label),1)],2))}}),h=re(T,[["__scopeId","data-v-d77c56d2"]]);T.__docgenInfo={exportName:"default",displayName:"CspSwitch",type:1,props:[{name:"label",global:!1,description:"",tags:[],required:!0,type:"string",declarations:[],schema:"string"},{name:"disabled",global:!1,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]},default:"false"},{name:"name",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"id",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string",default:"useId()"},{name:"size",global:!1,description:"",tags:[],required:!1,type:'"md" | "sm" | "lg"',declarations:[],schema:{kind:"enum",type:'"md" | "sm" | "lg"',schema:['"md"','"sm"','"lg"']},default:'"md"'},{name:"error",global:!1,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]},default:"false"},{name:"modelValue",global:!1,description:"",tags:[],required:!0,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"key",global:!0,description:"",tags:[],required:!1,type:"PropertyKey",declarations:[],schema:{kind:"enum",type:"PropertyKey",schema:["string","number","symbol"]}},{name:"ref",global:!0,description:"",tags:[],required:!1,type:"VNodeRef",declarations:[],schema:{kind:"enum",type:"VNodeRef",schema:["string","Ref<any, any>",{kind:"event",type:"(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void"}]}},{name:"ref_for",global:!0,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"ref_key",global:!0,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"class",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"},{name:"style",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"}],events:[{name:"update:modelValue",description:"",tags:[],type:"[value: boolean]",signature:'(event: "update:modelValue", value: boolean): void',declarations:[],schema:[{kind:"enum",type:"boolean",schema:["false","true"]}]}],slots:[],exposed:[{name:"error",type:"boolean",description:"",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"size",type:'"md" | "sm" | "lg"',description:"",declarations:[],schema:{kind:"enum",type:'"md" | "sm" | "lg"',schema:['"md"','"sm"','"lg"']}},{name:"disabled",type:"boolean",description:"",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"id",type:"string",description:"",declarations:[],schema:"string"},{name:"name",type:"string",description:"",declarations:[],schema:"string"},{name:"label",type:"string",description:"",declarations:[],schema:"string"},{name:"modelValue",type:"boolean",description:"",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}}],sourceFiles:"/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspSwitch/CspSwitch.vue"};const ke={title:"Éléments/Génériques/CspSwitch",component:h,tags:["autodocs"],parameters:{controls:{include:["modelValue","label","size","disabled","name","id","error"]},docs:{description:{component:"Bascule activé/désactivé"}}},argTypes:{modelValue:{control:{type:"boolean"},description:"État activé/désactivé (v-model).",table:{type:{summary:"boolean"}}},label:{control:{type:"text"},description:"Libellé visible associé à la bascule.",table:{type:{summary:"string"}}},disabled:{control:{type:"boolean"},description:"Désactive la bascule.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},name:{control:{type:"text"},description:"Attribut `name` pour la soumission de formulaire.",table:{type:{summary:"string"}}},id:{control:{type:"text"},description:"Attribut `id` du bouton bascule.",table:{type:{summary:"string"}}},error:{control:{type:"boolean"},description:"Affiche la bascule en état d'erreur.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},size:{control:{type:"radio"},options:["sm","md","lg"],description:"Taille de la bascule.",table:{type:{summary:"'sm' | 'md' | 'lg'"},defaultValue:{summary:"'md'"}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{modelValue:!1,label:"Libellé de la bascule",disabled:!1,name:void 0,id:void 0,size:"md",error:!1},render:a=>({components:{CspSwitch:h},setup(){const l=m(!!a.modelValue);return ee(()=>a.modelValue,e=>{l.value=!!e}),{args:a,value:l}},template:`
      <CspSwitch v-bind="args" v-model="value" />
    `})},i={},d={args:{disabled:!0}},u={args:{error:!0}},c={render:()=>({components:{CspSwitch:h},setup(){const a=m(!0),l=m(!0),e=m(!0);return{a,b:l,c:e}},template:`
      <div style="display: flex; gap: 3rem; align-items: flex-start;">
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">sm</span>
          <CspSwitch v-model="a" label="Option" size="sm" />
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">md</span>
          <CspSwitch v-model="b" label="Option" size="md" />
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">lg</span>
          <CspSwitch v-model="c" label="Option" size="lg" />
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}};var q,S,C;i.parameters={...i.parameters,docs:{...(q=i.parameters)==null?void 0:q.docs,source:{originalSource:"{}",...(C=(S=i.parameters)==null?void 0:S.docs)==null?void 0:C.source}}};var _,x,z;d.parameters={...d.parameters,docs:{...(_=d.parameters)==null?void 0:_.docs,source:{originalSource:`{
  args: {
    disabled: true
  }
}`,...(z=(x=d.parameters)==null?void 0:x.docs)==null?void 0:z.source}}};var B,R,O;u.parameters={...u.parameters,docs:{...(B=u.parameters)==null?void 0:B.docs,source:{originalSource:`{
  args: {
    error: true
  }
}`,...(O=(R=u.parameters)==null?void 0:R.docs)==null?void 0:O.source}}};var E,N,P;c.parameters={...c.parameters,docs:{...(E=c.parameters)==null?void 0:E.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspSwitch
    },
    setup() {
      const a = ref(true);
      const b = ref(true);
      const c = ref(true);
      return {
        a,
        b,
        c
      };
    },
    template: \`
      <div style="display: flex; gap: 3rem; align-items: flex-start;">
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">sm</span>
          <CspSwitch v-model="a" label="Option" size="sm" />
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">md</span>
          <CspSwitch v-model="b" label="Option" size="md" />
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">lg</span>
          <CspSwitch v-model="c" label="Option" size="lg" />
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...(P=(N=c.parameters)==null?void 0:N.docs)==null?void 0:P.source}}};const qe=["Default","Disabled","WithError","Sizes"];export{i as Default,d as Disabled,c as Sizes,u as WithError,qe as __namedExportsOrder,ke as default};
