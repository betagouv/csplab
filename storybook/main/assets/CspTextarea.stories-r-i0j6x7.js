import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{$ as t,C as n,D as r,E as i,F as a,H as o,I as s,O as c,Ot as l,St as u,Tt as d,X as f,Y as p,Z as m,c as h,ht as g,it as _,p as v,w as y,x as b}from"./iframe-kccjvU-D.js";import{n as x,t as S}from"./CspIcon-B6tDg2cG.js";import{n as C,t as w}from"./_plugin-vue_export-helper-BqBa3wPr.js";var T,E,D,O;function k(){return(k=e((()=>{h(),x(),T=[`for`],E=[`id`,`placeholder`,`rows`,`disabled`,`aria-invalid`],D={key:1,class:`csp-textarea-group__error`,role:`alert`},O=c({inheritAttrs:!1,__name:`CspTextarea`,props:a({placeholder:{},rows:{default:4},disabled:{type:Boolean,default:!1},error:{type:Boolean,default:!1},errorMessage:{},resize:{default:`vertical`},id:{default:()=>f()},label:{default:void 0}},{modelValue:{default:``},modelModifiers:{}}),emits:[`update:modelValue`],setup(e){let t=e,a=m(e,`modelValue`),c=p();return(f,p)=>(o(),y(`div`,{class:d([`csp-textarea-group`,{"csp-textarea-group--error":e.error}])},[e.label?(o(),y(`label`,{key:0,class:`csp-textarea-group__label`,for:e.id},l(e.label),9,T)):n(``,!0),_(b(`textarea`,s(u(c),{id:e.id,"onUpdate:modelValue":p[0]||=e=>a.value=e,class:[`csp-textarea`,[`csp-textarea--resize-${t.resize}`,{"csp-textarea--error":t.error}]],placeholder:t.placeholder,rows:t.rows,disabled:t.disabled,"aria-invalid":e.error||void 0}),null,16,E),[[v,a.value]]),e.error&&e.errorMessage?(o(),y(`p`,D,[r(S,{name:`ri:error-warning-fill`,size:14}),i(` `+l(e.errorMessage),1)])):n(``,!0)],2))}})})))()}var A;function j(){return(j=e((()=>{k(),C(),A=w(O,[[`__scopeId`,`data-v-35dd6122`]])})))()}var M,N,P,F,I,L,R,z,B;function V(){return(V=e((()=>{h(),j(),M=`base-textarea-story`,N={title:`Éléments/Génériques/CspTextarea`,component:A,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`placeholder`,`rows`,`disabled`,`error`,`errorMessage`,`resize`,`label`]},docs:{description:{component:"Primitive de zone de texte générique, contrôlée via `v-model` (`modelValue` / `update:modelValue`)."}}},argTypes:{modelValue:{control:{type:`text`},description:`Valeur actuelle de la zone de texte (v-model).`,table:{type:{summary:`string`}}},placeholder:{control:{type:`text`},description:`Espace réservé natif affiché lorsque le champ est vide.`,table:{type:{summary:`string`}}},rows:{control:{type:`number`,min:1,max:20},description:`Nombre de lignes visibles.`,table:{type:{summary:`number`},defaultValue:{summary:`4`}}},disabled:{control:{type:`boolean`},description:`Désactive la saisie de l'utilisateur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},error:{control:{type:`boolean`},description:`Affiche le champ en état d'erreur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},errorMessage:{control:{type:`text`},description:"Message d'erreur optionnel, affiché lorsque `error` est actif.",table:{type:{summary:`string`}}},resize:{control:{type:`radio`},options:[`none`,`vertical`,`horizontal`,`both`],description:`Comportement de redimensionnement natif.`,table:{type:{summary:`none | vertical | horizontal | both`},defaultValue:{summary:`vertical`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{modelValue:``,placeholder:`Tapez votre message…`,rows:4,disabled:!1,resize:`vertical`},render:e=>({components:{CspTextarea:A},setup(){let n=g(e.modelValue??``);t(()=>e.modelValue,e=>{n.value=e??``});function r(e){n.value=e}return{args:e,value:n,onUpdate:r,textareaId:M}},template:`
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
    `})},z={args:{label:`Message`,error:!0,errorMessage:`Ce champ est obligatoire.`,placeholder:`Tapez votre message…`,modelValue:``},render:e=>({components:{CspTextarea:A},setup(){let n=g(e.modelValue??``);return t(()=>e.modelValue,e=>{n.value=e??``}),{args:e,value:n}},template:`
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