import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{C as t,Ct as n,D as r,E as i,Et as a,F as o,H as s,I as c,O as l,Ot as u,X as d,Y as f,Z as p,at as m,b as h,c as g,d as _,et as v,gt as y,kt as b,w as x,x as S}from"./iframe-CO8wjsOU.js";import{n as C,t as w}from"./CspIcon-BiAOeQ2l.js";import{n as T,t as E}from"./_plugin-vue_export-helper-BqBa3wPr.js";var D,O,k,A,j,M;function N(){return(N=e((()=>{g(),C(),D=[`for`],O={key:0,class:`csp-input-group__hint`},k=[`id`,`name`,`type`,`placeholder`,`disabled`,`aria-invalid`,`aria-describedby`],A=[`id`],j={key:0,class:`csp-input-group__error`},M=l({inheritAttrs:!1,__name:`CspInput`,props:o({type:{default:`text`},placeholder:{},size:{default:`md`},disabled:{type:Boolean,default:!1},error:{type:Boolean,default:!1},errorMessage:{},id:{default:()=>d()},name:{},label:{},hint:{}},{modelValue:{default:``},modelModifiers:{}}),emits:[`update:modelValue`],setup(e){let o=p(e,`modelValue`),l=f(),d=h(()=>{let{class:e,style:t,...n}=l;return n});return(f,p)=>(s(),x(`div`,{class:a([`csp-input-group`,[n(l).class,{"csp-input-group--error":e.error}]]),style:u(n(l).style)},[e.label?(s(),x(`label`,{key:0,class:`csp-input-group__label`,for:e.id},[i(b(e.label)+` `,1),e.hint?(s(),x(`span`,O,b(e.hint),1)):t(``,!0)],8,D)):t(``,!0),m(S(`input`,c(d.value,{id:e.id,"onUpdate:modelValue":p[0]||=e=>o.value=e,name:e.name,type:e.type,placeholder:e.placeholder,disabled:e.disabled,"aria-invalid":e.error||void 0,"aria-describedby":`${e.id}-messages`,class:[`csp-input`,[`csp-input--${e.size}`,{"csp-input--error":e.error}]]}),null,16,k),[[_,o.value]]),S(`div`,{id:`${e.id}-messages`,class:`csp-input-group__messages`,"aria-live":`polite`},[e.error&&e.errorMessage?(s(),x(`p`,j,[r(w,{name:`ri:error-warning-fill`,size:14}),i(` `+b(e.errorMessage),1)])):t(``,!0)],8,A)],6))}})})))()}var P;function F(){return(F=e((()=>{N(),T(),P=E(M,[[`__scopeId`,`data-v-adda8ade`]]),M.__docgenInfo=Object.assign({displayName:M.name??M.__name},{exportName:`default`,displayName:`CspInput`,type:1,props:[{name:`type`,global:!1,default:`"text"`,description:``,tags:[],required:!1,type:`"number" | "text" | "search" | "email" | "password" | "tel" | "url" | undefined`,schema:{kind:`enum`,type:`"number" | "text" | "search" | "email" | "password" | "tel" | "url" | undefined`,schema:[`undefined`,`"number"`,`"text"`,`"search"`,`"email"`,`"password"`,`"tel"`,`"url"`]},declarations:[]},{name:`placeholder`,global:!1,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`size`,global:!1,default:`"md"`,description:``,tags:[],required:!1,type:`"md" | "sm" | "lg" | undefined`,schema:{kind:`enum`,type:`"md" | "sm" | "lg" | undefined`,schema:[`undefined`,`"md"`,`"sm"`,`"lg"`]},declarations:[]},{name:`disabled`,global:!1,default:`false`,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`error`,global:!1,default:`false`,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`errorMessage`,global:!1,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`id`,global:!1,default:`useId()`,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`name`,global:!1,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`label`,global:!1,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`hint`,global:!1,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`modelValue`,global:!1,default:`""`,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey | undefined`,schema:{kind:`enum`,type:`PropertyKey | undefined`,schema:[`undefined`,`string`,`number`,`symbol`]},declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef | undefined`,schema:{kind:`enum`,type:`VNodeRef | undefined`,schema:[`undefined`,`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any> | null, refs: Record<...>): void`}]},declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[{name:`update:modelValue`,description:``,tags:[],type:`[value: string]`,signature:`(event: "update:modelValue", value: string): void`,schema:[`string`],declarations:[]}],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/components/base/CspInput/CspInput.vue`})})))()}var I,L,R,z,B,V,H,U,W;function G(){return(G=e((()=>{g(),F(),I={title:`Éléments/Génériques/CspInput`,component:P,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`type`,`placeholder`,`size`,`disabled`,`error`,`errorMessage`,`id`,`name`,`label`,`hint`]},docs:{description:{component:`Champ de saisie de texte.`}}},argTypes:{modelValue:{control:{type:`text`},description:`Valeur actuelle (v-model).`,table:{type:{summary:`string`}}},type:{control:{type:`radio`},options:[`text`,`email`,`password`,`search`,`tel`,`url`,`number`],description:`Type d'entrée natif.`,table:{type:{summary:`text | email | password | search | tel | url | number`},defaultValue:{summary:`text`}}},placeholder:{control:{type:`text`},description:`Texte d'espace réservé (placeholder).`,table:{type:{summary:`string`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille de l'entrée.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},disabled:{control:{type:`boolean`},description:`Désactive l'entrée.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},error:{control:{type:`boolean`},description:`Affiche le champ en état d'erreur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},errorMessage:{control:{type:`text`},description:"Message d'erreur optionnel, affiché lorsque `error` est actif.",table:{type:{summary:`string`}}},id:{control:{type:`text`},description:`ID optionnel pour l'association du label.`,table:{type:{summary:`string`}}},name:{control:{type:`text`},description:`Nom optionnel pour la soumission du formulaire.`,table:{type:{summary:`string`}}},hint:{control:{type:`text`},description:`Aide affichée sous le libellé, dont elle fait partie et qui la porte dans le nom accessible.`,table:{type:{summary:`string`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{modelValue:``,type:`text`,placeholder:`Saisir un texte`,size:`md`,disabled:!1,id:`base-input-story`,name:`base-input`,label:`Libellé`},render:e=>({components:{CspInput:P},setup(){let t=y(e.modelValue??``);v(()=>e.modelValue,e=>{t.value=e??``});function n(e){t.value=e}return{args:e,value:t,handleUpdate:n}},template:`
      <div class="w-96">
        <CspInput
          v-bind="args"
          :model-value="value"
          @update:model-value="handleUpdate"
        />
      </div>
    `})},L=[`sm`,`md`,`lg`],R=[`text`,`email`,`password`,`search`,`tel`,`url`,`number`],z={},B={args:{disabled:!0,modelValue:`Valeur non modifiable`}},V={render:e=>({components:{CspInput:P},setup(){return{sizes:L,args:e}},template:`
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
    `})},H={render:e=>({components:{CspInput:P},setup(){return{types:R,args:e}},template:`
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
    `})},U={args:{label:`Libellé input`,error:!0,errorMessage:`Ce champ est obligatoire.`,modelValue:``},render:e=>({components:{CspInput:P},setup(){let t=y(e.modelValue??``);return v(()=>e.modelValue,e=>{t.value=e??``}),{args:e,value:t}},template:`
      <div class="w-96">
        <CspInput
          v-bind="args"
          :model-value="value"
          @update:model-value="value = $event"
        />
      </div>
    `})},W=[`Default`,`Disabled`,`Sizes`,`Types`,`WithError`],z.parameters={...z.parameters,docs:{...z.parameters?.docs,source:{originalSource:`{}`,...z.parameters?.docs?.source}}},B.parameters={...B.parameters,docs:{...B.parameters?.docs,source:{originalSource:`{
  args: {
    disabled: true,
    modelValue: 'Valeur non modifiable'
  }
}`,...B.parameters?.docs?.source}}},V.parameters={...V.parameters,docs:{...V.parameters?.docs,source:{originalSource:`{
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
}`,...V.parameters?.docs?.source}}},H.parameters={...H.parameters,docs:{...H.parameters?.docs,source:{originalSource:`{
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
}`,...H.parameters?.docs?.source}}},U.parameters={...U.parameters,docs:{...U.parameters?.docs,source:{originalSource:`{
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
}`,...U.parameters?.docs?.source}}}})))()}G();export{z as Default,B as Disabled,V as Sizes,H as Types,U as WithError,W as __namedExportsOrder,I as default};