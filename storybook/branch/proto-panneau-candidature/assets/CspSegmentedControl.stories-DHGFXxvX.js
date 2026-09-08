import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{C as t,Ct as n,D as r,Et as i,G as a,I as o,Q as s,S as c,U as l,Z as u,_ as d,at as f,c as p,et as m,f as h,gt as g,k as _,kt as v,w as y,x as b}from"./iframe-BUHbOAUL.js";import{n as x,t as S}from"./CspIcon-Dwk_Md1L.js";import{n as C,t as w}from"./_plugin-vue_export-helper-BqBa3wPr.js";var T,E,D,O,k;function A(){return(A=e((()=>{p(),x(),T=[`disabled`],E={class:`csp-segmented__elements`},D=[`id`,`name`,`value`,`disabled`],O=[`for`],k=_({__name:`CspSegmentedControl`,props:o({options:{},legend:{},hideLegend:{type:Boolean,default:!1},inlineLegend:{type:Boolean,default:!1},size:{default:`md`},name:{default:void 0},disabled:{type:Boolean,default:!1}},{modelValue:{required:!0},modelModifiers:{}}),emits:[`update:modelValue`],setup(e){let o=e,p=s(e,`modelValue`),m=o.name??u();return(o,s)=>(l(),y(`fieldset`,{class:i([`csp-segmented`,[`csp-segmented--${e.size}`,{"csp-segmented--no-legend":e.hideLegend}]]),disabled:e.disabled},[b(`legend`,{class:i([`csp-segmented__legend`,{"csp-segmented__legend--inline":e.inlineLegend}])},v(e.legend),3),b(`div`,E,[(l(!0),y(d,null,a(e.options,e=>(l(),y(`div`,{key:e.value,class:`csp-segmented__element`},[f(b(`input`,{id:`${n(m)}-${e.value}`,"onUpdate:modelValue":s[0]||=e=>p.value=e,type:`radio`,name:n(m),value:e.value,disabled:e.disabled},null,8,D),[[h,p.value]]),b(`label`,{for:`${n(m)}-${e.value}`},[e.icon?(l(),c(S,{key:0,name:e.icon,class:`csp-segmented__icon`},null,8,[`name`])):t(``,!0),r(` `+v(e.label),1)],8,O)]))),128))])],10,T))}})})))()}var j;function M(){return(M=e((()=>{A(),C(),j=w(k,[[`__scopeId`,`data-v-e5918664`]])})))()}var N,P,F,I,L,R,z,B,V,H;function U(){return(U=e((()=>{p(),M(),N=[{value:`option-1`,label:`Option 1`},{value:`option-2`,label:`Option 2`},{value:`option-3`,label:`Option 3`}],P=[{value:`grille`,label:`Grille`,icon:`ri:layout-grid-line`},{value:`liste`,label:`Liste`,icon:`ri:list-unordered`}],F={title:`Éléments/Génériques/CspSegmentedControl`,component:j,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`options`,`legend`,`hideLegend`,`inlineLegend`,`size`,`disabled`]},docs:{description:{component:"Contrôle segmenté du DSFR : une option unique parmi deux à cinq, liée via `v-model`. La légende est obligatoire ; `hideLegend` la réserve aux lecteurs d'écran."}}},argTypes:{modelValue:{control:{type:`text`},description:`Valeur sélectionnée.`,table:{type:{summary:`string`}}},options:{control:{type:`object`},description:`Options du contrôle.`,table:{type:{summary:`{ value: string; label: string; icon?: string; disabled?: boolean }[]`}}},legend:{control:{type:`text`},description:`Légende du groupe, toujours présente pour les technologies d'assistance.`},hideLegend:{control:{type:`boolean`},description:`Masque visuellement la légende.`},inlineLegend:{control:{type:`boolean`},description:`Affiche la légende sur la même ligne que le contrôle.`},size:{control:{type:`select`},options:[`sm`,`md`],table:{defaultValue:{summary:`md`}}},disabled:{control:{type:`boolean`},description:`Désactive tout le groupe.`}},args:{modelValue:`option-1`,options:N,legend:`Choix`,hideLegend:!1,inlineLegend:!1,size:`md`,disabled:!1},render:e=>({components:{CspSegmentedControl:j},setup(){let t=g(e.modelValue);return m(()=>e.modelValue,e=>{t.value=e}),{args:e,model:t}},template:`<CspSegmentedControl v-bind="args" v-model="model" />`})},I={},L={args:{inlineLegend:!0}},R={args:{hideLegend:!0}},z={args:{options:P,modelValue:`grille`,legend:`Affichage`,hideLegend:!0}},B={render:()=>({components:{CspSegmentedControl:j},setup(){return{md:g(`grille`),sm:g(`grille`),options:P}},template:`
      <div style="display: flex; flex-direction: column; gap: 1rem; align-items: flex-start;">
        <CspSegmentedControl v-model="md" :options="options" legend="Taille md" inline-legend />
        <CspSegmentedControl v-model="sm" :options="options" legend="Taille sm" inline-legend size="sm" />
      </div>
    `})},V={render:()=>({components:{CspSegmentedControl:j},setup(){return{partial:g(`option-1`),disabled:g(`option-1`),options:[...N.slice(0,2),{value:`option-3`,label:`Option 3`,disabled:!0}],DEFAULT_OPTIONS:N}},template:`
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