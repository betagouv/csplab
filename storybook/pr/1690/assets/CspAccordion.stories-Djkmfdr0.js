import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{i as t,n,r,t as i}from"./CspAccordionItem-BfWtFsqH.js";var a,o,s,c,l,u,d,f,p;function m(){return(m=e((()=>{t(),n(),a=[{value:`item-1`,title:`Première question`,content:`Réponse à la première question.`},{value:`item-2`,title:`Deuxième question`,content:`Réponse à la deuxième question.`},{value:`item-3`,title:`Troisième question`,content:`Réponse à la troisième question.`}],o={title:`Éléments/Génériques/CspAccordion`,component:r,tags:[`autodocs`],parameters:{controls:{include:[`type`,`collapsible`,`defaultValue`]},docs:{description:{component:"Accordéon accessible basé sur Reka UI. Placez un `CspAccordionItem` (`value`, `title`, contenu en slot) par section dépliable. Chaque titre est un bouton dans un `<h3>` par défaut (prop `headingLevel` du `CspAccordionItem` pour l'ajuster au plan de la page), avec `aria-expanded` et `aria-controls` ; les flèches, Début et Fin passent d'un titre à l'autre au sein d'un même accordéon."}}},argTypes:{type:{control:{type:`radio`},options:[`single`,`multiple`],description:`Une seule section ouverte à la fois, ou plusieurs.`,table:{type:{summary:`'single' | 'multiple'`},defaultValue:{summary:`'multiple'`}}},collapsible:{control:{type:`boolean`},description:"En mode `single`, permet de refermer la section ouverte.",table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},defaultValue:{control:{type:`object`},description:`Section(s) ouverte(s) au premier rendu.`,table:{type:{summary:`string | string[]`}}}},args:{type:`multiple`,collapsible:!0},render:e=>({components:{CspAccordion:r,CspAccordionItem:i},setup(){return{args:e,items:a}},template:`
      <CspAccordion v-bind="args">
        <CspAccordionItem
          v-for="item in items"
          :key="item.value"
          :value="item.value"
          :title="item.title"
        >
          <p>{{ item.content }}</p>
        </CspAccordionItem>
      </CspAccordion>
    `})},s={name:`Par défaut`},c={name:`Ouvert par défaut`,args:{defaultValue:[`item-1`]}},l={name:`Une section à la fois`,args:{type:`single`,defaultValue:`item-1`}},u={name:`Plusieurs sections ouvertes`,args:{type:`multiple`,defaultValue:[`item-1`,`item-3`]}},d=`Une réponse longue, découpée en paragraphes et en liste, pour vérifier le retour à la ligne et l'espacement.
- Premier point de la liste, assez long pour passer sur plusieurs lignes lorsque la largeur disponible est réduite.
- Deuxième point de la liste.
- Troisième point de la liste.

Un dernier paragraphe conclut la réponse et rappelle où trouver plus d'informations.`,f={name:`Contenu long`,args:{defaultValue:[`item-long`]},render:e=>({components:{CspAccordion:r,CspAccordionItem:i},setup(){return{args:e,content:d,items:a.slice(1)}},template:`
      <CspAccordion v-bind="args">
        <CspAccordionItem
          value="item-long"
          title="Une question dont la réponse est longue et dont le titre lui-même s'étend sur plusieurs lignes quand la place manque"
        >
          <p style="white-space: pre-line">{{ content }}</p>
        </CspAccordionItem>
        <CspAccordionItem
          v-for="item in items"
          :key="item.value"
          :value="item.value"
          :title="item.title"
        >
          <p>{{ item.content }}</p>
        </CspAccordionItem>
      </CspAccordion>
    `})},p=[`Default`,`OuvertParDefaut`,`Single`,`PlusieursOuvertes`,`ContenuLong`],s.parameters={...s.parameters,docs:{...s.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...s.parameters?.docs?.source}}},c.parameters={...c.parameters,docs:{...c.parameters?.docs,source:{originalSource:`{
  name: 'Ouvert par défaut',
  args: {
    defaultValue: ['item-1']
  }
}`,...c.parameters?.docs?.source}}},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
  name: 'Une section à la fois',
  args: {
    type: 'single',
    defaultValue: 'item-1'
  }
}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  name: 'Plusieurs sections ouvertes',
  args: {
    type: 'multiple',
    defaultValue: ['item-1', 'item-3']
  }
}`,...u.parameters?.docs?.source}}},f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
  name: 'Contenu long',
  args: {
    defaultValue: ['item-long']
  },
  render: (args: CspAccordionProps) => ({
    components: {
      CspAccordion,
      CspAccordionItem
    },
    setup() {
      return {
        args,
        content: LONG_CONTENT,
        items: ITEMS.slice(1)
      };
    },
    template: \`
      <CspAccordion v-bind="args">
        <CspAccordionItem
          value="item-long"
          title="Une question dont la réponse est longue et dont le titre lui-même s'étend sur plusieurs lignes quand la place manque"
        >
          <p style="white-space: pre-line">{{ content }}</p>
        </CspAccordionItem>
        <CspAccordionItem
          v-for="item in items"
          :key="item.value"
          :value="item.value"
          :title="item.title"
        >
          <p>{{ item.content }}</p>
        </CspAccordionItem>
      </CspAccordion>
    \`
  })
}`,...f.parameters?.docs?.source}}}})))()}m();export{f as ContenuLong,s as Default,c as OuvertParDefaut,u as PlusieursOuvertes,l as Single,p as __namedExportsOrder,o as default};