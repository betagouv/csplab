import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{g as t,t as n,yt as r}from"./vue.esm-bundler-BdiU-5Kf.js";import{n as i,t as a}from"./CspButton-DefoOEn5.js";import{n as o,t as s}from"./CspCheckboxGroup-CRR2yOqy.js";import{n as c,t as l}from"./CspFiltersDrawer-jpKdKjdb.js";var u,d,f;function p(){return(p=e((()=>{n(),i(),o(),c(),u={title:`Compositions/Génériques/CspFiltersDrawer`,component:l,tags:[`autodocs`],parameters:{controls:{disable:!0},docs:{description:{component:"Tiroir de filtres : les champs passés dans le slot par défaut, suivis des boutons « Appliquer les filtres » et « Réinitialiser ». Émet `apply` et `reset` ; `canReset` active la réinitialisation."}}},args:{open:!1,canReset:!1},render:()=>({components:{CspButton:a,CspCheckboxGroup:s,CspFiltersDrawer:l},setup(){let e=r(!1),n=r([]);return{open:e,statuts:n,canReset:t(()=>n.value.length>0),options:[{value:`brouillon`,label:`Brouillon`},{value:`publie`,label:`Publié`},{value:`archive`,label:`Archivé`}]}},template:`
      <CspButton
        label="Filtres"
        variant="tertiary"
        icon="ri:filter-line"
        is-icon-left
        @click="open = true"
      />
      <CspFiltersDrawer
        v-model:open="open"
        :can-reset="canReset"
        @apply="open = false"
        @reset="statuts = []"
      >
        <CspCheckboxGroup
          v-model="statuts"
          label="Statut"
          :options="options"
        />
      </CspFiltersDrawer>
    `})},d={},f=[`Default`],d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{}`,...d.parameters?.docs?.source}}}})))()}p();export{d as Default,f as __namedExportsOrder,u as default};