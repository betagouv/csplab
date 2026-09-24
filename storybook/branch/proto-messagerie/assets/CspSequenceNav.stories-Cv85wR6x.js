import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{b as t,c as n,ht as r}from"./iframe-yO-s4GRX.js";import{n as i,t as a}from"./CspSequenceNav-CpfvEo2n.js";var o,s,c,l,u,d,f;function p(){return(p=e((()=>{n(),i(),o={title:`Éléments/Génériques/CspSequenceNav`,component:a,tags:[`autodocs`],parameters:{docs:{description:{component:"Navigation séquentielle entre les éléments d’une liste : boutons Précédent et Suivant, et compteur de position annoncé aux technologies d’assistance. Le composant ne connaît pas la liste : il reçoit la position, le total et l’état de chaque bouton, et émet `previous` et `next`. Le slot par défaut ajoute un contexte au-dessus du compteur."}}},argTypes:{position:{control:{type:`number`,min:1},description:"Position de l’élément courant, à partir de 1. `null` quand la position est inconnue : le compteur est masqué."},total:{control:{type:`number`,min:0},description:`Nombre total d’éléments.`},itemLabel:{control:`text`,description:`Nom de l’élément affiché dans le compteur.`,table:{defaultValue:{summary:`Élément`}}},label:{control:`text`,description:`Nom accessible de la navigation.`,table:{defaultValue:{summary:`Navigation entre les éléments`}}},previousDisabled:{control:`boolean`},nextDisabled:{control:`boolean`}},args:{position:2,total:4,itemLabel:`Élément`,previousDisabled:!1,nextDisabled:!1}},s={name:`Par défaut`},c={name:`Premier élément`,args:{position:1,previousDisabled:!0}},l={name:`Position inconnue`,args:{position:null,previousDisabled:!0,nextDisabled:!0}},u={name:`Avec un contexte`,render:e=>({components:{CspSequenceNav:a},setup:()=>({args:e}),template:`
      <CspSequenceNav v-bind="args">
        Dossier : En cours
      </CspSequenceNav>
    `})},d={render:()=>({components:{CspSequenceNav:a},setup(){let e=r(1);return{total:5,position:e,isFirst:t(()=>e.value===1),isLast:t(()=>e.value===5)}},template:`
      <CspSequenceNav
        :position="position"
        :total="total"
        item-label="Page"
        :previous-disabled="isFirst"
        :next-disabled="isLast"
        @previous="position--"
        @next="position++"
      />
    `})},f=[`Defaut`,`PremierElement`,`PositionInconnue`,`AvecContexte`,`Interactif`],s.parameters={...s.parameters,docs:{...s.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...s.parameters?.docs?.source}}},c.parameters={...c.parameters,docs:{...c.parameters?.docs,source:{originalSource:`{
  name: 'Premier élément',
  args: {
    position: 1,
    previousDisabled: true
  }
}`,...c.parameters?.docs?.source}}},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
  name: 'Position inconnue',
  args: {
    position: null,
    previousDisabled: true,
    nextDisabled: true
  }
}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  name: 'Avec un contexte',
  render: args => ({
    components: {
      CspSequenceNav
    },
    setup: () => ({
      args
    }),
    template: \`
      <CspSequenceNav v-bind="args">
        Dossier : En cours
      </CspSequenceNav>
    \`
  })
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspSequenceNav
    },
    setup() {
      const total = 5;
      const position = ref(1);
      return {
        total,
        position,
        isFirst: computed(() => position.value === 1),
        isLast: computed(() => position.value === total)
      };
    },
    template: \`
      <CspSequenceNav
        :position="position"
        :total="total"
        item-label="Page"
        :previous-disabled="isFirst"
        :next-disabled="isLast"
        @previous="position--"
        @next="position++"
      />
    \`
  })
}`,...d.parameters?.docs?.source}}}})))()}p();export{u as AvecContexte,s as Defaut,d as Interactif,l as PositionInconnue,c as PremierElement,f as __namedExportsOrder,o as default};