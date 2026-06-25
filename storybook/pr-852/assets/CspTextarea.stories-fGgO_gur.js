import{i as e}from"./preload-helper-DnyzYt22.js";import{$ as t,D as n,G as r,H as i,Ht as a,It as o,Q as s,U as c,V as l,W as u,at as d,dt as f,ft as p,ht as m,j as h,kt as g,pt as _,yt as v,z as y,zt as b}from"./iframe-NvCSxVNi.js";import{n as x,t as S}from"./_plugin-vue_export-helper-CdXk-eJM.js";import{n as C,t as w}from"./CspIcon-CHGxhXtY.js";var T,E,D,O,k=e((()=>{n(),C(),T=[`for`],E=[`id`,`placeholder`,`rows`,`disabled`,`aria-invalid`],D={key:1,class:`csp-textarea-group__error`,role:`alert`},O=r({inheritAttrs:!1,__name:`CspTextarea`,props:s({placeholder:{},rows:{default:4},disabled:{type:Boolean,default:!1},error:{type:Boolean,default:!1},errorMessage:{},resize:{default:`vertical`},id:{default:()=>p()},label:{default:void 0}},{modelValue:{default:``},modelModifiers:{}}),emits:[`update:modelValue`],setup(e){let n=e,r=_(e,`modelValue`),s=f();return(f,p)=>(d(),i(`div`,{class:b([`csp-textarea-group`,{"csp-textarea-group--error":e.error}])},[e.label?(d(),i(`label`,{key:0,class:`csp-textarea-group__label`,for:e.id},a(e.label),9,T)):l(``,!0),v(y(`textarea`,t(o(s),{id:e.id,"onUpdate:modelValue":p[0]||=e=>r.value=e,class:[`csp-textarea`,[`csp-textarea--resize-${n.resize}`,{"csp-textarea--error":n.error}]],placeholder:n.placeholder,rows:n.rows,disabled:n.disabled,"aria-invalid":e.error||void 0}),null,16,E),[[h,r.value]]),e.error&&e.errorMessage?(d(),i(`p`,D,[u(w,{name:`ri:error-warning-fill`,size:14}),c(` `+a(e.errorMessage),1)])):l(``,!0)],2))}})})),A=e((()=>{})),j,M=e((()=>{k(),k(),A(),x(),j=S(O,[[`__scopeId`,`data-v-35dd6122`]]),O.__docgenInfo=Object.assign({displayName:O.name??O.__name},{exportName:`default`,displayName:`CspTextarea`,type:1,props:[{name:`error`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`resize`,global:!1,description:``,tags:[],required:!1,type:`"vertical" | "none" | "horizontal" | "both"`,declarations:[],schema:{kind:`enum`,type:`"vertical" | "none" | "horizontal" | "both"`,schema:[`"vertical"`,`"none"`,`"horizontal"`,`"both"`]},default:`"vertical"`},{name:`label`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`undefined`},{name:`disabled`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`id`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`useId()`},{name:`rows`,global:!1,description:``,tags:[],required:!1,type:`number`,declarations:[],schema:`number`,default:`4`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`errorMessage`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`modelValue`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`""`},{name:`placeholder`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`}],events:[{name:`update:modelValue`,description:``,tags:[],type:`[value: string]`,signature:`(event: "update:modelValue", value: string): void`,declarations:[],schema:[`string`]}],slots:[],exposed:[{name:`error`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`resize`,type:`"vertical" | "none" | "horizontal" | "both"`,description:``,declarations:[],schema:{kind:`enum`,type:`"vertical" | "none" | "horizontal" | "both"`,schema:[`"vertical"`,`"none"`,`"horizontal"`,`"both"`]}},{name:`label`,type:`string`,description:``,declarations:[],schema:`string`},{name:`disabled`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`id`,type:`string`,description:``,declarations:[],schema:`string`},{name:`rows`,type:`number`,description:``,declarations:[],schema:`number`},{name:`errorMessage`,type:`string`,description:``,declarations:[],schema:`string`},{name:`modelValue`,type:`string`,description:``,declarations:[],schema:`string`},{name:`placeholder`,type:`string`,description:``,declarations:[],schema:`string`}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspTextarea/CspTextarea.vue`})})),N,P,F,I,L,R,z,B,V;e((()=>{n(),M(),N=`base-textarea-story`,P={title:`Éléments/Génériques/CspTextarea`,component:j,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`placeholder`,`rows`,`disabled`,`error`,`errorMessage`,`resize`,`label`]},docs:{description:{component:"Primitive de zone de texte générique, contrôlée via `v-model` (`modelValue` / `update:modelValue`)."}}},argTypes:{modelValue:{control:{type:`text`},description:`Valeur actuelle de la zone de texte (v-model).`,table:{type:{summary:`string`}}},placeholder:{control:{type:`text`},description:`Espace réservé natif affiché lorsque le champ est vide.`,table:{type:{summary:`string`}}},rows:{control:{type:`number`,min:1,max:20},description:`Nombre de lignes visibles.`,table:{type:{summary:`number`},defaultValue:{summary:`4`}}},disabled:{control:{type:`boolean`},description:`Désactive la saisie de l'utilisateur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},error:{control:{type:`boolean`},description:`Affiche le champ en état d'erreur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},errorMessage:{control:{type:`text`},description:"Message d'erreur optionnel, affiché lorsque `error` est actif.",table:{type:{summary:`string`}}},resize:{control:{type:`radio`},options:[`none`,`vertical`,`horizontal`,`both`],description:`Comportement de redimensionnement natif.`,table:{type:{summary:`none | vertical | horizontal | both`},defaultValue:{summary:`vertical`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{modelValue:``,placeholder:`Tapez votre message…`,rows:4,disabled:!1,resize:`vertical`},render:e=>({components:{CspTextarea:j},setup(){let t=g(e.modelValue??``);m(()=>e.modelValue,e=>{t.value=e??``});function n(e){t.value=e}return{args:e,value:t,onUpdate:n,textareaId:N}},template:`
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
    `})},F=[`none`,`vertical`,`horizontal`,`both`],I={},L={render:e=>({components:{CspTextarea:j},setup(){return{args:e}},template:`
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
    `})},R={render:e=>({components:{CspTextarea:j},setup(){return{args:e,resizes:F}},template:`
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
    `})},z={render:e=>({components:{CspTextarea:j},setup(){return{args:e,rowsVariants:[2,4,8]}},template:`
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
    `})},B={args:{label:`Message`,error:!0,errorMessage:`Ce champ est obligatoire.`,placeholder:`Tapez votre message…`,modelValue:``},render:e=>({components:{CspTextarea:j},setup(){let t=g(e.modelValue??``);return m(()=>e.modelValue,e=>{t.value=e??``}),{args:e,value:t}},template:`
      <div class="max-w-xl">
        <CspTextarea
          v-bind="args"
          :model-value="value"
          @update:model-value="value = $event"
        />
      </div>
    `})},I.parameters={...I.parameters,docs:{...I.parameters?.docs,source:{originalSource:`{}`,...I.parameters?.docs?.source}}},L.parameters={...L.parameters,docs:{...L.parameters?.docs,source:{originalSource:`{
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
}`,...L.parameters?.docs?.source}}},R.parameters={...R.parameters,docs:{...R.parameters?.docs,source:{originalSource:`{
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
}`,...R.parameters?.docs?.source}}},z.parameters={...z.parameters,docs:{...z.parameters?.docs,source:{originalSource:`{
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
}`,...z.parameters?.docs?.source}}},B.parameters={...B.parameters,docs:{...B.parameters?.docs,source:{originalSource:`{
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
}`,...B.parameters?.docs?.source}}},V=[`Default`,`States`,`Resizes`,`Rows`,`WithError`]}))();export{I as Default,R as Resizes,z as Rows,L as States,B as WithError,V as __namedExportsOrder,P as default};