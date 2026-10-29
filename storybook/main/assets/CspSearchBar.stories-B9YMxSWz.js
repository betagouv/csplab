import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{c as t,ht as n}from"./iframe-B2DcHKH-.js";import{n as r,t as i}from"./CspSearchBar-ZS0bTO6k.js";function a(e){return{components:{CspSearchBar:i},setup(){return{args:e,value:n(``),submitted:n(``)}},template:`
      <div style="max-width: 32rem;">
        <CspSearchBar v-bind="args" v-model="value" @search="submitted = $event" />
        <p v-if="submitted" style="margin-top: 1rem; font-size: 0.875rem; color: var(--text-mention-grey);">Recherche lancée : {{ submitted }}</p>
      </div>
    `}}var o,s,c,l,u,d,f,p,m;function h(){return(h=e((()=>{t(),r(),o={title:`Éléments/Génériques/CspSearchBar`,component:i,tags:[`autodocs`],parameters:{controls:{include:[`label`,`mode`,`hideLabel`,`hint`,`placeholder`,`size`,`disabled`,`error`,`errorMessage`,`buttonLabel`]},docs:{description:{component:"Barre de recherche DSFR, en deux modes. En mode `submit`, par défaut, la recherche se lance à la validation : un bouton accompagne le champ, et l’événement `search` porte la valeur sans espaces superflus au clic ou à la touche Entrée. En mode `live`, la recherche suit la saisie par le `v-model` : le bouton disparaît et une loupe discrète signale le champ de recherche. La touche Entrée émet toujours `search`, pour appliquer un filtre qui attend une pause dans la frappe. Le libellé peut être masqué visuellement dans une barre d’outils, il reste le nom accessible du champ. Deux tailles : MD pour une recherche contextuelle, LG pour un moteur mis en avant."}}},argTypes:{mode:{control:`radio`,options:[`submit`,`live`]},size:{control:`radio`,options:[`md`,`lg`]}},args:{label:`Rechercher`,placeholder:`Rechercher`,size:`md`}},s={render:a},c={name:`Filtre au fil de la saisie`,args:{mode:`live`,hideLabel:!0,placeholder:`Filtrer la liste`},render:a},l={args:{size:`lg`},render:a},u={name:`Libellé masqué`,args:{hideLabel:!0},render:a},d={name:`Avec indication`,args:{label:`Adresse email`,hint:`Adresse complète du compte`,placeholder:`prenom.nom@exemple.gouv.fr`},render:a},f={args:{error:!0,errorMessage:`Aucun résultat pour cette recherche.`},render:a},p={args:{disabled:!0},render:a},m=[`Default`,`Live`,`Large`,`HiddenLabel`,`WithHint`,`Error`,`Disabled`],s.parameters={...s.parameters,docs:{...s.parameters?.docs,source:{originalSource:`{
  render
}`,...s.parameters?.docs?.source}}},c.parameters={...c.parameters,docs:{...c.parameters?.docs,source:{originalSource:`{
  name: 'Filtre au fil de la saisie',
  args: {
    mode: 'live',
    hideLabel: true,
    placeholder: 'Filtrer la liste'
  },
  render
}`,...c.parameters?.docs?.source}}},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
  args: {
    size: 'lg'
  },
  render
}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  name: 'Libellé masqué',
  args: {
    hideLabel: true
  },
  render
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
  name: 'Avec indication',
  args: {
    label: 'Adresse email',
    hint: 'Adresse complète du compte',
    placeholder: 'prenom.nom@exemple.gouv.fr'
  },
  render
}`,...d.parameters?.docs?.source}}},f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
  args: {
    error: true,
    errorMessage: 'Aucun résultat pour cette recherche.'
  },
  render
}`,...f.parameters?.docs?.source}}},p.parameters={...p.parameters,docs:{...p.parameters?.docs,source:{originalSource:`{
  args: {
    disabled: true
  },
  render
}`,...p.parameters?.docs?.source}}}})))()}h();export{s as Default,p as Disabled,f as Error,u as HiddenLabel,l as Large,c as Live,d as WithHint,m as __namedExportsOrder,o as default};