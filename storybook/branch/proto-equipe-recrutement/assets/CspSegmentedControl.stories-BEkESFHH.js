import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{_t as t,l as n,tt as r}from"./iframe-C0OAurLG.js";import{n as i,t as a}from"./CspSegmentedControl-6YpJZrvF.js";var o,s,c,l,u,d,f,p,m,h;function g(){return(g=e((()=>{n(),i(),o=[{value:`option-1`,label:`Option 1`},{value:`option-2`,label:`Option 2`},{value:`option-3`,label:`Option 3`}],s=[{value:`grille`,label:`Grille`,icon:`ri:layout-grid-line`},{value:`liste`,label:`Liste`,icon:`ri:list-unordered`}],c={title:`Éléments/Génériques/CspSegmentedControl`,component:a,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`options`,`legend`,`hideLegend`,`inlineLegend`,`size`,`disabled`]},docs:{description:{component:"Contrôle segmenté du DSFR : une option unique parmi deux à cinq, liée via `v-model`. La légende est obligatoire ; `hideLegend` la réserve aux lecteurs d'écran."}}},argTypes:{modelValue:{control:{type:`text`},description:`Valeur sélectionnée.`,table:{type:{summary:`string`}}},options:{control:{type:`object`},description:`Options du contrôle.`,table:{type:{summary:`{ value: string; label: string; icon?: string; disabled?: boolean }[]`}}},legend:{control:{type:`text`},description:`Légende du groupe, toujours présente pour les technologies d'assistance.`},hideLegend:{control:{type:`boolean`},description:`Masque visuellement la légende.`},inlineLegend:{control:{type:`boolean`},description:`Affiche la légende sur la même ligne que le contrôle.`},size:{control:{type:`select`},options:[`sm`,`md`],table:{defaultValue:{summary:`md`}}},disabled:{control:{type:`boolean`},description:`Désactive tout le groupe.`}},args:{modelValue:`option-1`,options:o,legend:`Choix`,hideLegend:!1,inlineLegend:!1,size:`md`,disabled:!1},render:e=>({components:{CspSegmentedControl:a},setup(){let n=t(e.modelValue);return r(()=>e.modelValue,e=>{n.value=e}),{args:e,model:n}},template:`<CspSegmentedControl v-bind="args" v-model="model" />`})},l={},u={args:{inlineLegend:!0}},d={args:{hideLegend:!0}},f={args:{options:s,modelValue:`grille`,legend:`Affichage`,hideLegend:!0}},p={render:()=>({components:{CspSegmentedControl:a},setup(){return{md:t(`grille`),sm:t(`grille`),options:s}},template:`
      <div style="display: flex; flex-direction: column; gap: 1rem; align-items: flex-start;">
        <CspSegmentedControl v-model="md" :options="options" legend="Taille md" inline-legend />
        <CspSegmentedControl v-model="sm" :options="options" legend="Taille sm" inline-legend size="sm" />
      </div>
    `})},m={render:()=>({components:{CspSegmentedControl:a},setup(){return{partial:t(`option-1`),disabled:t(`option-1`),options:[...o.slice(0,2),{value:`option-3`,label:`Option 3`,disabled:!0}],DEFAULT_OPTIONS:o}},template:`
      <div style="display: flex; flex-direction: column; gap: 1rem; align-items: flex-start;">
        <CspSegmentedControl v-model="partial" :options="options" legend="Une option désactivée" inline-legend />
        <CspSegmentedControl v-model="disabled" :options="DEFAULT_OPTIONS" legend="Groupe désactivé" inline-legend disabled />
      </div>
    `})},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  args: {
    inlineLegend: true
  }
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
  args: {
    hideLegend: true
  }
}`,...d.parameters?.docs?.source}}},f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
  args: {
    options: ICON_OPTIONS,
    modelValue: 'grille',
    legend: 'Affichage',
    hideLegend: true
  }
}`,...f.parameters?.docs?.source}}},p.parameters={...p.parameters,docs:{...p.parameters?.docs,source:{originalSource:`{
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
}`,...p.parameters?.docs?.source}}},m.parameters={...m.parameters,docs:{...m.parameters?.docs,source:{originalSource:`{
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
}`,...m.parameters?.docs?.source}}},h=[`Default`,`InlineLegend`,`NoLegend`,`WithIcons`,`Sizes`,`States`]})))()}g();export{l as Default,u as InlineLegend,d as NoLegend,p as Sizes,m as States,f as WithIcons,h as __namedExportsOrder,c as default};