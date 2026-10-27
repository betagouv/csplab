import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{t,yt as n}from"./vue.esm-bundler-BdiU-5Kf.js";import{n as r,t as i}from"./CspButton-Djj-IYhA.js";import{n as a,t as o}from"./CspUnsavedChangesDialog-CgjxlXU9.js";var s,c,l;function u(){return(u=e((()=>{t(),r(),a(),s={title:`Éléments/Génériques/CspUnsavedChangesDialog`,component:o,tags:[`autodocs`],parameters:{controls:{disable:!0},docs:{description:{component:"Confirmation demandée avant de quitter une saisie non enregistrée. Émet `keepEditing` sur « Continuer l'édition », la touche Échap et le clic en dehors, et `leave` sur « Quitter sans enregistrer ». Se pilote avec `useUnsavedChangesGuard`."}}},args:{open:!1},render:()=>({components:{CspButton:i,CspUnsavedChangesDialog:o},setup(){return{open:n(!1)}},template:`
      <CspButton
        label="Quitter la saisie"
        variant="primary"
        @click="open = true"
      />
      <CspUnsavedChangesDialog
        :open="open"
        @keep-editing="open = false"
        @leave="open = false"
      />
    `})},c={},l=[`Default`],c.parameters={...c.parameters,docs:{...c.parameters?.docs,source:{originalSource:`{}`,...c.parameters?.docs?.source}}}})))()}u();export{c as Default,l as __namedExportsOrder,s as default};