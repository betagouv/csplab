import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{n as t,t as n}from"./CspBadge-VQrXo-c8.js";import{n as r,t as i}from"./CspButton-D2C_4CnW.js";import{n as a,t as o}from"./CspPageHeader-C95uZnKS.js";var s,c,l,u,d,f,p,m;function h(){return(h=e((()=>{t(),r(),a(),s={title:`Compositions/Génériques/CspPageHeader`,component:o,tags:[`autodocs`],parameters:{controls:{include:[`title`,`breadcrumb`]},docs:{description:{component:"En-tête de page : fil d’Ariane + titre (prop `title`), avec un lien de retour optionnel (`backLink`), les slots `#actions` et `#subtitle`, et des skeletons de chargement (`showTitleSkeleton`, `showSubtitleSkeleton`)."}}},argTypes:{title:{control:{type:`text`},description:"Titre de la page (rendu dans le `<h1>`).",table:{type:{summary:`string`}}},breadcrumb:{control:{type:`object`},description:`Maillons du fil d’Ariane, délégués à CspBreadcrumb.`,table:{type:{summary:`{ label: string; to?: RouteLocationRaw }[]`}}},backLink:{control:{type:`object`},description:`Lien de retour optionnel affiché avant le titre.`,table:{type:{summary:`{ to: RouteLocationRaw; label: string }`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}}},args:{title:`Titre de la page`,breadcrumb:[{label:`Accueil`,to:`/`},{label:`Section`},{label:`Page courante`}]}},c={name:`Par défaut`},l={name:`Sans fil d’Ariane`,args:{breadcrumb:[]}},u={name:`Avec actions`,render:e=>({components:{CspPageHeader:o,CspButton:i},setup(){return{args:e}},template:`
      <CspPageHeader v-bind="args">
        <template #actions>
          <CspButton variant="tertiary" icon="ri:filter-3-line" label="Action secondaire" :is-icon-left="true" />
          <CspButton icon="ri:add-line" label="Action principale" :is-icon-left="true" />
        </template>
      </CspPageHeader>
    `})},d={name:`Avec sous-titre`,render:e=>({components:{CspPageHeader:o,CspBadge:n},setup(){return{args:e}},template:`
      <CspPageHeader v-bind="args">
        <template #subtitle>
          <span>Métadonnée</span>
          <CspBadge type="success" label="Statut" />
        </template>
      </CspPageHeader>
    `})},f={name:`Avec lien de retour`,args:{backLink:{to:`/`,label:`Retour`}}},p={name:`Chargement`,args:{showTitleSkeleton:!0,showSubtitleSkeleton:!0}},c.parameters={...c.parameters,docs:{...c.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...c.parameters?.docs?.source}}},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
  name: 'Sans fil d’Ariane',
  args: {
    breadcrumb: []
  }
}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
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
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
  name: 'Avec sous-titre',
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
}`,...d.parameters?.docs?.source}}},f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
  name: 'Avec lien de retour',
  args: {
    backLink: {
      to: '/',
      label: 'Retour'
    }
  }
}`,...f.parameters?.docs?.source}}},p.parameters={...p.parameters,docs:{...p.parameters?.docs,source:{originalSource:`{
  name: 'Chargement',
  args: {
    showTitleSkeleton: true,
    showSubtitleSkeleton: true
  }
}`,...p.parameters?.docs?.source}}},m=[`Default`,`WithoutBreadcrumb`,`WithActions`,`WithSubtitle`,`WithBackLink`,`Loading`]})))()}h();export{c as Default,p as Loading,u as WithActions,f as WithBackLink,d as WithSubtitle,l as WithoutBreadcrumb,m as __namedExportsOrder,s as default};