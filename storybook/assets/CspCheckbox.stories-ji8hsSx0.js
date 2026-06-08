import{K as a,a1 as m}from"./vue.esm-bundler-By9fcp0_.js";import{a as d}from"./CspCheckbox-CzRFkOdQ.js";import"./useForwardExpose-X_C_In--.js";import"./nullish-CHIgUVhi.js";import"./RovingFocusItem-B9cFdH4s.js";import"./Presence-CbBynXIb.js";import"./Primitive-DkO9CfBM.js";import"./VisuallyHiddenInput-ChDZSDGw.js";import"./_plugin-vue_export-helper-DlAUqK2U.js";const U={title:"Éléments/Génériques/CspCheckbox",component:d,tags:["autodocs"],parameters:{controls:{include:["modelValue","label","size","disabled","indeterminate","error"]},docs:{description:{component:"Primitive de case à cocher générique. Contrôlée via `modelValue` (v-model). L'état optionnel `indeterminate` est uniquement visuel et doit être contrôlé par le parent."}}},argTypes:{modelValue:{control:{type:"boolean"},description:"État coché (v-model).",table:{type:{summary:"boolean"}}},label:{control:{type:"text"},description:"Libellé visible.",table:{type:{summary:"string"}}},disabled:{control:{type:"boolean"},description:"Désactive la case à cocher.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},indeterminate:{control:{type:"boolean"},description:"Visuel à trois états : affiche un état indéterminé. Le parent doit le réinitialiser lors d'une interaction utilisateur.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},size:{control:{type:"radio"},options:["sm","md","lg"],description:"Taille de la case à cocher.",table:{type:{summary:"'sm' | 'md' | 'lg'"},defaultValue:{summary:"'md'"}}},error:{control:{type:"boolean"},description:"Affiche la case à cocher en état d'erreur.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{modelValue:!1,label:"Accepter les conditions",disabled:!1,indeterminate:!1,size:"md",error:!1},render:e=>({components:{CspCheckbox:d},setup(){const t=a(!!e.modelValue),s=a(!!e.indeterminate);m(()=>e.modelValue,l=>{t.value=!!l}),m(()=>e.indeterminate,l=>{s.value=!!l});function O(l){t.value=l,s.value&&(s.value=!1)}return{args:e,value:t,isIndeterminate:s,handleUpdate:O}},template:`
      <div class="h-12 flex items-center">
        <CspCheckbox
          :label="args.label"
          :disabled="args.disabled"
          :indeterminate="isIndeterminate"
          :size="args.size"
          :model-value="value"
          @update:model-value="handleUpdate"
        />
      </div>
    `})},n={},o={args:{disabled:!0}},r={args:{indeterminate:!0,modelValue:!1}},c={render:()=>({components:{CspCheckbox:d},setup(){const e=a(!0),t=a(!1);return{checked:e,unchecked:t}},template:`
      <div class="flex flex-col gap-4">
        <CspCheckbox v-model="unchecked" label="Non coché" />
        <CspCheckbox v-model="checked" label="Coché" />
        <CspCheckbox :model-value="false" :indeterminate="true" label="Indéterminé" />
        <CspCheckbox :model-value="false" :disabled="true" label="Désactivé" />
      </div>
    `}),parameters:{controls:{disable:!0}}},i={render:()=>({components:{CspCheckbox:d},setup(){const e=a(!0),t=a(!0),s=a(!0);return{a:e,b:t,c:s}},template:`
      <div class="flex flex-row gap-12">
        <div class="flex flex-col gap-2">
          <span class="text-xs text-text-mention-grey">sm</span>
          <CspCheckbox v-model="a" label="Option" size="sm" />
        </div>
        <div class="flex flex-col gap-2">
          <span class="text-xs text-text-mention-grey">md</span>
          <CspCheckbox v-model="b" label="Option" size="md" />
        </div>
        <div class="flex flex-col gap-2">
          <span class="text-xs text-text-mention-grey">lg</span>
          <CspCheckbox v-model="c" label="Option" size="lg" />
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}};var p,u,b;n.parameters={...n.parameters,docs:{...(p=n.parameters)==null?void 0:p.docs,source:{originalSource:"{}",...(b=(u=n.parameters)==null?void 0:u.docs)==null?void 0:b.source}}};var f,x,v;o.parameters={...o.parameters,docs:{...(f=o.parameters)==null?void 0:f.docs,source:{originalSource:`{
  args: {
    disabled: true
  }
}`,...(v=(x=o.parameters)==null?void 0:x.docs)==null?void 0:v.source}}};var h,C,g;r.parameters={...r.parameters,docs:{...(h=r.parameters)==null?void 0:h.docs,source:{originalSource:`{
  args: {
    indeterminate: true,
    modelValue: false
  }
}`,...(g=(C=r.parameters)==null?void 0:C.docs)==null?void 0:g.source}}};var y,k,z;c.parameters={...c.parameters,docs:{...(y=c.parameters)==null?void 0:y.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspCheckbox
    },
    setup() {
      const checked = ref(true);
      const unchecked = ref(false);
      return {
        checked,
        unchecked
      };
    },
    template: \`
      <div class="flex flex-col gap-4">
        <CspCheckbox v-model="unchecked" label="Non coché" />
        <CspCheckbox v-model="checked" label="Coché" />
        <CspCheckbox :model-value="false" :indeterminate="true" label="Indéterminé" />
        <CspCheckbox :model-value="false" :disabled="true" label="Désactivé" />
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...(z=(k=c.parameters)==null?void 0:k.docs)==null?void 0:z.source}}};var V,S,D;i.parameters={...i.parameters,docs:{...(V=i.parameters)==null?void 0:V.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspCheckbox
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
      <div class="flex flex-row gap-12">
        <div class="flex flex-col gap-2">
          <span class="text-xs text-text-mention-grey">sm</span>
          <CspCheckbox v-model="a" label="Option" size="sm" />
        </div>
        <div class="flex flex-col gap-2">
          <span class="text-xs text-text-mention-grey">md</span>
          <CspCheckbox v-model="b" label="Option" size="md" />
        </div>
        <div class="flex flex-col gap-2">
          <span class="text-xs text-text-mention-grey">lg</span>
          <CspCheckbox v-model="c" label="Option" size="lg" />
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...(D=(S=i.parameters)==null?void 0:S.docs)==null?void 0:D.source}}};const E=["Default","Disabled","Indeterminate","States","Sizes"];export{n as Default,o as Disabled,r as Indeterminate,i as Sizes,c as States,E as __namedExportsOrder,U as default};
