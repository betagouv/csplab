import{R as v,C as i}from"./CspRadio-DZlaS0Zb.js";import{O as z}from"./vue.esm-bundler-7zVN4DZj.js";import"./useForwardExpose-qwf_wVRM.js";import"./RovingFocusItem-DT9Z5IoK.js";import"./useId-Blg3GNwK.js";import"./Primitive-DzgJnGz8.js";import"./Collection-C9Lj7FBv.js";import"./ConfigProvider-lmrMonQJ.js";import"./usePrimitiveElement-BQ6g5-es.js";import"./RovingFocusGroup-DzvvbqBY.js";import"./useFormControl-5LFzebFo.js";import"./VisuallyHiddenInput-CPKKsE9z.js";import"./VisuallyHidden-BOK6EsXA.js";import"./handleAndDispatchCustomEvent-ChOKVcqp.js";import"./ohash.D__AXeF1-Cq3NGnZa.js";import"./Presence-CGGvXRHO.js";import"./_plugin-vue_export-helper-DlAUqK2U.js";const q={title:"Éléments/Génériques/CspRadio",component:i,tags:["autodocs"],parameters:{controls:{include:["value","label","size","disabled","error"]},docs:{description:{component:"Bouton radio basé sur reka-ui. Doit être utilisé à l'intérieur de `CspRadioGroup` (ou d'un `RadioGroupRoot`). La navigation clavier entre les éléments (flèches) et la gestion du nom de formulaire sont assurées par le groupe parent."}}},argTypes:{value:{control:{type:"text"},description:"Valeur de cet élément radio.",table:{type:{summary:"string"}}},label:{control:{type:"text"},description:"Libellé texte visible associé au bouton radio.",table:{type:{summary:"string"}}},disabled:{control:{type:"boolean"},description:"Désactive ce bouton radio.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},size:{control:{type:"radio"},options:["sm","md","lg"],description:"Taille du bouton radio.",table:{type:{summary:"'sm' | 'md' | 'lg'"},defaultValue:{summary:"'md'"}}},error:{control:{type:"boolean"},description:"Affiche le bouton radio en état d'erreur.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{value:"option-a",label:"Option A",disabled:!1,size:"md",error:!1},render:s=>({components:{CspRadio:i,RadioGroupRoot:v},setup(){const a=z("option-a");return{args:s,selected:a}},template:`
      <RadioGroupRoot v-model="selected">
        <CspRadio v-bind="args" />
      </RadioGroupRoot>
    `})},e={},o={args:{disabled:!0}},r={render:()=>({components:{CspRadio:i,RadioGroupRoot:v},setup(){const s=["sm","md","lg"],a=z("option-md");return{sizes:s,selected:a}},template:`
      <RadioGroupRoot
        v-model="selected"
        class="flex flex-row gap-12"
      >
      <div
        v-for="size in sizes"
        :key="size"
      >
        <div class="h-12 flex items-center">
            <CspRadio
              :value="'option-' + size"
              :label="'Option ' + size.toUpperCase()"
              :size="size"
            />
          </div>
        </div>
      </RadioGroupRoot>
    `})},t={args:{error:!0}};var l,d,p;e.parameters={...e.parameters,docs:{...(l=e.parameters)==null?void 0:l.docs,source:{originalSource:"{}",...(p=(d=e.parameters)==null?void 0:d.docs)==null?void 0:p.source}}};var n,u,m;o.parameters={...o.parameters,docs:{...(n=o.parameters)==null?void 0:n.docs,source:{originalSource:`{
  args: {
    disabled: true
  }
}`,...(m=(u=o.parameters)==null?void 0:u.docs)==null?void 0:m.source}}};var c,b,f;r.parameters={...r.parameters,docs:{...(c=r.parameters)==null?void 0:c.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspRadio,
      RadioGroupRoot
    },
    setup() {
      const sizes = ['sm', 'md', 'lg'];
      const selected = ref('option-md');
      return {
        sizes,
        selected
      };
    },
    template: \`
      <RadioGroupRoot
        v-model="selected"
        class="flex flex-row gap-12"
      >
      <div
        v-for="size in sizes"
        :key="size"
      >
        <div class="h-12 flex items-center">
            <CspRadio
              :value="'option-' + size"
              :label="'Option ' + size.toUpperCase()"
              :size="size"
            />
          </div>
        </div>
      </RadioGroupRoot>
    \`
  })
}`,...(f=(b=r.parameters)==null?void 0:b.docs)==null?void 0:f.source}}};var R,y,g;t.parameters={...t.parameters,docs:{...(R=t.parameters)==null?void 0:R.docs,source:{originalSource:`{
  args: {
    error: true
  }
}`,...(g=(y=t.parameters)==null?void 0:y.docs)==null?void 0:g.source}}};const B=["Default","Disabled","Sizes","WithError"];export{e as Default,o as Disabled,r as Sizes,t as WithError,B as __namedExportsOrder,q as default};
