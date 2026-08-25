import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{C as t,D as n,Dt as r,E as i,F as a,J as o,P as s,Q as c,S as l,T as u,V as d,X as f,Y as p,b as m,c as h,f as g,mt as _,rt as v,wt as y,xt as b}from"./iframe-DVYIelxs.js";import{n as x,t as S}from"./CspIcon-r0NrkG0F.js";import{n as C,t as w}from"./_plugin-vue_export-helper-BqBa3wPr.js";var T,E,D,O;function k(){return(k=e((()=>{h(),x(),T=[`for`],E=[`id`,`placeholder`,`rows`,`disabled`,`aria-invalid`],D={key:1,class:`csp-textarea-group__error`,role:`alert`},O=n({inheritAttrs:!1,__name:`CspTextarea`,props:s({placeholder:{},rows:{default:4},disabled:{type:Boolean,default:!1},error:{type:Boolean,default:!1},errorMessage:{},resize:{default:`vertical`},id:{default:()=>p()},label:{default:void 0}},{modelValue:{default:``},modelModifiers:{}}),emits:[`update:modelValue`],setup(e){let n=e,s=f(e,`modelValue`),c=o();return(o,f)=>(d(),t(`div`,{class:y([`csp-textarea-group`,{"csp-textarea-group--error":e.error}])},[e.label?(d(),t(`label`,{key:0,class:`csp-textarea-group__label`,for:e.id},r(e.label),9,T)):l(``,!0),v(m(`textarea`,a(b(c),{id:e.id,"onUpdate:modelValue":f[0]||=e=>s.value=e,class:[`csp-textarea`,[`csp-textarea--resize-${n.resize}`,{"csp-textarea--error":n.error}]],placeholder:n.placeholder,rows:n.rows,disabled:n.disabled,"aria-invalid":e.error||void 0}),null,16,E),[[g,s.value]]),e.error&&e.errorMessage?(d(),t(`p`,D,[i(S,{name:`ri:error-warning-fill`,size:14}),u(` `+r(e.errorMessage),1)])):l(``,!0)],2))}})})))()}var A;function j(){return(j=e((()=>{k(),C(),A=w(O,[[`__scopeId`,`data-v-35dd6122`]])})))()}var M,N,P,F,I,L,R,z,B;function V(){return(V=e((()=>{h(),j(),M=`base-textarea-story`,N={title:`Éléments/Génériques/CspTextarea`,component:A,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`placeholder`,`rows`,`disabled`,`error`,`errorMessage`,`resize`,`label`]},docs:{description:{component:"Primitive de zone de texte générique, contrôlée via `v-model` (`modelValue` / `update:modelValue`)."}}},argTypes:{modelValue:{control:{type:`text`},description:`Valeur actuelle de la zone de texte (v-model).`,table:{type:{summary:`string`}}},placeholder:{control:{type:`text`},description:`Espace réservé natif affiché lorsque le champ est vide.`,table:{type:{summary:`string`}}},rows:{control:{type:`number`,min:1,max:20},description:`Nombre de lignes visibles.`,table:{type:{summary:`number`},defaultValue:{summary:`4`}}},disabled:{control:{type:`boolean`},description:`Désactive la saisie de l'utilisateur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},error:{control:{type:`boolean`},description:`Affiche le champ en état d'erreur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},errorMessage:{control:{type:`text`},description:"Message d'erreur optionnel, affiché lorsque `error` est actif.",table:{type:{summary:`string`}}},resize:{control:{type:`radio`},options:[`none`,`vertical`,`horizontal`,`both`],description:`Comportement de redimensionnement natif.`,table:{type:{summary:`none | vertical | horizontal | both`},defaultValue:{summary:`vertical`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{modelValue:``,placeholder:`Tapez votre message…`,rows:4,disabled:!1,resize:`vertical`},render:e=>({components:{CspTextarea:A},setup(){let t=_(e.modelValue??``);c(()=>e.modelValue,e=>{t.value=e??``});function n(e){t.value=e}return{args:e,value:t,onUpdate:n,textareaId:M}},template:`
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
    `})},P=[`none`,`vertical`,`horizontal`,`both`],F={},I={render:e=>({components:{CspTextarea:A},setup(){return{args:e}},template:`
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
    `})},L={render:e=>({components:{CspTextarea:A},setup(){return{args:e,resizes:P}},template:`
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
    `})},R={render:e=>({components:{CspTextarea:A},setup(){return{args:e,rowsVariants:[2,4,8]}},template:`
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
    `})},z={args:{label:`Message`,error:!0,errorMessage:`Ce champ est obligatoire.`,placeholder:`Tapez votre message…`,modelValue:``},render:e=>({components:{CspTextarea:A},setup(){let t=_(e.modelValue??``);return c(()=>e.modelValue,e=>{t.value=e??``}),{args:e,value:t}},template:`
      <div class="max-w-xl">
        <CspTextarea
          v-bind="args"
          :model-value="value"
          @update:model-value="value = $event"
        />
      </div>
    `})},F.parameters={...F.parameters,docs:{...F.parameters?.docs,source:{originalSource:`{}`,...F.parameters?.docs?.source}}},I.parameters={...I.parameters,docs:{...I.parameters?.docs,source:{originalSource:`{
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
}`,...I.parameters?.docs?.source}}},L.parameters={...L.parameters,docs:{...L.parameters?.docs,source:{originalSource:`{
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
}`,...L.parameters?.docs?.source}}},R.parameters={...R.parameters,docs:{...R.parameters?.docs,source:{originalSource:`{
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
}`,...R.parameters?.docs?.source}}},z.parameters={...z.parameters,docs:{...z.parameters?.docs,source:{originalSource:`{
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
}`,...z.parameters?.docs?.source}}},B=[`Default`,`States`,`Resizes`,`Rows`,`WithError`]})))()}V();export{F as Default,L as Resizes,R as Rows,I as States,z as WithError,B as __namedExportsOrder,N as default};