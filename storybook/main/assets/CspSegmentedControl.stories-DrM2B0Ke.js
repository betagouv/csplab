import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{$ as t,C as n,E as r,F as i,H as a,O as o,Ot as s,S as c,St as l,Tt as u,W as d,X as f,Z as p,_ as m,c as h,f as g,ht as _,it as v,w as y,x as b}from"./iframe-kccjvU-D.js";import{n as x,t as S}from"./CspIcon-B6tDg2cG.js";import{n as C,t as w}from"./_plugin-vue_export-helper-BqBa3wPr.js";var T,E,D,O,k;function A(){return(A=e((()=>{h(),x(),T=[`disabled`],E={class:`csp-segmented__elements`},D=[`id`,`name`,`value`,`disabled`],O=[`for`],k=o({__name:`CspSegmentedControl`,props:i({options:{},legend:{},hideLegend:{type:Boolean,default:!1},inlineLegend:{type:Boolean,default:!1},size:{default:`md`},name:{default:void 0},disabled:{type:Boolean,default:!1}},{modelValue:{required:!0},modelModifiers:{}}),emits:[`update:modelValue`],setup(e){let t=e,i=p(e,`modelValue`),o=t.name??f();return(t,f)=>(a(),y(`fieldset`,{class:u([`csp-segmented`,[`csp-segmented--${e.size}`,{"csp-segmented--no-legend":e.hideLegend}]]),disabled:e.disabled},[b(`legend`,{class:u([`csp-segmented__legend`,{"csp-segmented__legend--inline":e.inlineLegend}])},s(e.legend),3),b(`div`,E,[(a(!0),y(m,null,d(e.options,e=>(a(),y(`div`,{key:e.value,class:`csp-segmented__element`},[v(b(`input`,{id:`${l(o)}-${e.value}`,"onUpdate:modelValue":f[0]||=e=>i.value=e,type:`radio`,name:l(o),value:e.value,disabled:e.disabled},null,8,D),[[g,i.value]]),b(`label`,{for:`${l(o)}-${e.value}`},[e.icon?(a(),c(S,{key:0,name:e.icon,class:`csp-segmented__icon`},null,8,[`name`])):n(``,!0),r(` `+s(e.label),1)],8,O)]))),128))])],10,T))}})})))()}var j;function M(){return(M=e((()=>{A(),C(),j=w(k,[[`__scopeId`,`data-v-e5918664`]])})))()}var N,P,F,I,L,R,z,B,V,H;function U(){return(U=e((()=>{h(),M(),N=[{value:`option-1`,label:`Option 1`},{value:`option-2`,label:`Option 2`},{value:`option-3`,label:`Option 3`}],P=[{value:`grille`,label:`Grille`,icon:`ri:layout-grid-line`},{value:`liste`,label:`Liste`,icon:`ri:list-unordered`}],F={title:`Éléments/Génériques/CspSegmentedControl`,component:j,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`options`,`legend`,`hideLegend`,`inlineLegend`,`size`,`disabled`]},docs:{description:{component:"Contrôle segmenté du DSFR : une option unique parmi deux à cinq, liée via `v-model`. La légende est obligatoire ; `hideLegend` la réserve aux lecteurs d'écran."}}},argTypes:{modelValue:{control:{type:`text`},description:`Valeur sélectionnée.`,table:{type:{summary:`string`}}},options:{control:{type:`object`},description:`Options du contrôle.`,table:{type:{summary:`{ value: string; label: string; icon?: string; disabled?: boolean }[]`}}},legend:{control:{type:`text`},description:`Légende du groupe, toujours présente pour les technologies d'assistance.`},hideLegend:{control:{type:`boolean`},description:`Masque visuellement la légende.`},inlineLegend:{control:{type:`boolean`},description:`Affiche la légende sur la même ligne que le contrôle.`},size:{control:{type:`select`},options:[`sm`,`md`],table:{defaultValue:{summary:`md`}}},disabled:{control:{type:`boolean`},description:`Désactive tout le groupe.`}},args:{modelValue:`option-1`,options:N,legend:`Choix`,hideLegend:!1,inlineLegend:!1,size:`md`,disabled:!1},render:e=>({components:{CspSegmentedControl:j},setup(){let n=_(e.modelValue);return t(()=>e.modelValue,e=>{n.value=e}),{args:e,model:n}},template:`<CspSegmentedControl v-bind="args" v-model="model" />`})},I={},L={args:{inlineLegend:!0}},R={args:{hideLegend:!0}},z={args:{options:P,modelValue:`grille`,legend:`Affichage`,hideLegend:!0}},B={render:()=>({components:{CspSegmentedControl:j},setup(){return{md:_(`grille`),sm:_(`grille`),options:P}},template:`
      <div style="display: flex; flex-direction: column; gap: 1rem; align-items: flex-start;">
        <CspSegmentedControl v-model="md" :options="options" legend="Taille md" inline-legend />
        <CspSegmentedControl v-model="sm" :options="options" legend="Taille sm" inline-legend size="sm" />
      </div>
    `})},V={render:()=>({components:{CspSegmentedControl:j},setup(){return{partial:_(`option-1`),disabled:_(`option-1`),options:[...N.slice(0,2),{value:`option-3`,label:`Option 3`,disabled:!0}],DEFAULT_OPTIONS:N}},template:`
      <div style="display: flex; flex-direction: column; gap: 1rem; align-items: flex-start;">
        <CspSegmentedControl v-model="partial" :options="options" legend="Une option désactivée" inline-legend />
        <CspSegmentedControl v-model="disabled" :options="DEFAULT_OPTIONS" legend="Groupe désactivé" inline-legend disabled />
      </div>
    `})},I.parameters={...I.parameters,docs:{...I.parameters?.docs,source:{originalSource:`{}`,...I.parameters?.docs?.source}}},L.parameters={...L.parameters,docs:{...L.parameters?.docs,source:{originalSource:`{
  args: {
    inlineLegend: true
  }
}`,...L.parameters?.docs?.source}}},R.parameters={...R.parameters,docs:{...R.parameters?.docs,source:{originalSource:`{
  args: {
    hideLegend: true
  }
}`,...R.parameters?.docs?.source}}},z.parameters={...z.parameters,docs:{...z.parameters?.docs,source:{originalSource:`{
  args: {
    options: ICON_OPTIONS,
    modelValue: 'grille',
    legend: 'Affichage',
    hideLegend: true
  }
}`,...z.parameters?.docs?.source}}},B.parameters={...B.parameters,docs:{...B.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspSegmentedControl
    },
    setup() {
      const md = ref('grille');
      const sm = ref('grille');
      return {
        md,
        sm,
        options: ICON_OPTIONS
      };
    },
    template: \`
      <div style="display: flex; flex-direction: column; gap: 1rem; align-items: flex-start;">
        <CspSegmentedControl v-model="md" :options="options" legend="Taille md" inline-legend />
        <CspSegmentedControl v-model="sm" :options="options" legend="Taille sm" inline-legend size="sm" />
      </div>
    \`
  })
}`,...B.parameters?.docs?.source}}},V.parameters={...V.parameters,docs:{...V.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspSegmentedControl
    },
    setup() {
      const partial = ref('option-1');
      const disabled = ref('option-1');
      const options = [...DEFAULT_OPTIONS.slice(0, 2), {
        value: 'option-3',
        label: 'Option 3',
        disabled: true
      }];
      return {
        partial,
        disabled,
        options,
        DEFAULT_OPTIONS
      };
    },
    template: \`
      <div style="display: flex; flex-direction: column; gap: 1rem; align-items: flex-start;">
        <CspSegmentedControl v-model="partial" :options="options" legend="Une option désactivée" inline-legend />
        <CspSegmentedControl v-model="disabled" :options="DEFAULT_OPTIONS" legend="Groupe désactivé" inline-legend disabled />
      </div>
    \`
  })
}`,...V.parameters?.docs?.source}}},H=[`Default`,`InlineLegend`,`NoLegend`,`WithIcons`,`Sizes`,`States`]})))()}U();export{I as Default,L as InlineLegend,R as NoLegend,B as Sizes,V as States,z as WithIcons,H as __namedExportsOrder,F as default};