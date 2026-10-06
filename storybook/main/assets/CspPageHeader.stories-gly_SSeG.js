import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{n as t,t as n}from"./CspBadge-T-iUJ_vo.js";import{n as r,t as i}from"./CspButton-DVYS-XKD.js";import{n as a,t as o}from"./CspPageHeader-B4yauEpO.js";var s,c,l,u,d,f,p,m,h;function g(){return(g=e((()=>{t(),r(),a(),s={title:`Compositions/Génériques/CspPageHeader`,component:o,tags:[`autodocs`],parameters:{controls:{include:[`title`,`breadcrumb`]},docs:{description:{component:"En-tête de page : fil d’Ariane, titre (prop `title`) et sous-titre textuel (prop `subtitle`), avec un lien de retour optionnel (`backLink`), une largeur alignée sur le conteneur de page (`width`), les slots `#actions` et `#subtitle` pour un sous-titre riche, et des skeletons de chargement (`showTitleSkeleton`, `showSubtitleSkeleton`)."}}},argTypes:{title:{control:{type:`text`},description:"Titre de la page (rendu dans le `<h1>`).",table:{type:{summary:`string`}}},subtitle:{control:{type:`text`},description:"Sous-titre textuel sous le titre. Le slot `#subtitle` le remplace pour un contenu riche.",table:{type:{summary:`string`}}},breadcrumb:{control:{type:`object`},description:`Maillons du fil d’Ariane, délégués à CspBreadcrumb.`,table:{type:{summary:`{ label: string; to?: RouteLocationRaw }[]`}}},backLink:{control:{type:`object`},description:`Lien de retour optionnel affiché avant le titre.`,table:{type:{summary:`{ to: RouteLocationRaw; label: string }`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}}},args:{title:`Titre de la page`,breadcrumb:[{label:`Accueil`,to:`/`},{label:`Section`},{label:`Page courante`}]}},c={name:`Par défaut`},l={name:`Avec sous-titre textuel`,args:{subtitle:`Une phrase qui présente le contenu de la page.`}},u={name:`Sans fil d’Ariane`,args:{breadcrumb:[]}},d={name:`Avec actions`,render:e=>({components:{CspPageHeader:o,CspButton:i},setup(){return{args:e}},template:`
      <CspPageHeader v-bind="args">
        <template #actions>
          <CspButton variant="tertiary" icon="ri:filter-3-line" label="Action secondaire" :is-icon-left="true" />
          <CspButton icon="ri:add-line" label="Action principale" :is-icon-left="true" />
        </template>
      </CspPageHeader>
    `})},f={name:`Avec sous-titre riche`,render:e=>({components:{CspPageHeader:o,CspBadge:n},setup(){return{args:e}},template:`
      <CspPageHeader v-bind="args">
        <template #subtitle>
          <span>Métadonnée</span>
          <CspBadge type="success" label="Statut" />
        </template>
      </CspPageHeader>
    `})},p={name:`Avec lien de retour`,args:{backLink:{to:`/`,label:`Retour`}}},m={name:`Chargement`,args:{showTitleSkeleton:!0,showSubtitleSkeleton:!0}},h=[`Default`,`WithTextSubtitle`,`WithoutBreadcrumb`,`WithActions`,`WithSubtitle`,`WithBackLink`,`Loading`],c.parameters={...c.parameters,docs:{...c.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...c.parameters?.docs?.source}}},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
  name: 'Avec sous-titre textuel',
  args: {
    subtitle: 'Une phrase qui présente le contenu de la page.'
  }
}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  name: 'Sans fil d’Ariane',
  args: {
    breadcrumb: []
  }
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
  name: 'Avec actions',
  render: (args: CspPageHeaderProps) => ({
    components: {
      CspPageHeader,
      CspButton
    },
    setup() {
      return {
        args
      };
    },
    template: \`
      <CspPageHeader v-bind="args">
        <template #actions>
          <CspButton variant="tertiary" icon="ri:filter-3-line" label="Action secondaire" :is-icon-left="true" />
          <CspButton icon="ri:add-line" label="Action principale" :is-icon-left="true" />
        </template>
      </CspPageHeader>
    \`
  })
}`,...d.parameters?.docs?.source}}},f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
  name: 'Avec sous-titre riche',
  render: (args: CspPageHeaderProps) => ({
    components: {
      CspPageHeader,
      CspBadge
    },
    setup() {
      return {
        args
      };
    },
    template: \`
      <CspPageHeader v-bind="args">
        <template #subtitle>
          <span>Métadonnée</span>
          <CspBadge type="success" label="Statut" />
        </template>
      </CspPageHeader>
    \`
  })
}`,...f.parameters?.docs?.source}}},p.parameters={...p.parameters,docs:{...p.parameters?.docs,source:{originalSource:`{
  name: 'Avec lien de retour',
  args: {
    backLink: {
      to: '/',
      label: 'Retour'
    }
  }
}`,...p.parameters?.docs?.source}}},m.parameters={...m.parameters,docs:{...m.parameters?.docs,source:{originalSource:`{
  name: 'Chargement',
  args: {
    showTitleSkeleton: true,
    showSubtitleSkeleton: true
  }
}`,...m.parameters?.docs?.source}}}})))()}g();export{c as Default,m as Loading,d as WithActions,p as WithBackLink,f as WithSubtitle,l as WithTextSubtitle,u as WithoutBreadcrumb,h as __namedExportsOrder,s as default};