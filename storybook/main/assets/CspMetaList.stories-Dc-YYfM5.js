import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{C as t,D as n,H as r,I as i,O as a,Tt as o,W as s,_ as c,b as l,c as u,w as d}from"./iframe-CnJ3gxPo.js";import{n as f,t as p}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{n as m,t as h}from"./CspMeta-Bd05k1dG.js";var g;function _(){return(_=e((()=>{u(),m(),g=a({__name:`CspMetaList`,props:{items:{},size:{default:`md`},layout:{default:`inline`}},setup(e){let a=e,u=l(()=>a.items.filter(e=>e.label)),f=l(()=>[`csp-meta-list`,`csp-meta-list--${a.layout}`,`csp-meta-list--${a.size}`]);return(a,l)=>u.value.length?(r(),d(`ul`,{key:0,class:o(f.value)},[(r(!0),d(c,null,s(u.value,(t,a)=>(r(),d(`li`,{key:`${t.label}-${a}`,class:`csp-meta-list__item`},[n(h,i({ref_for:!0},t,{size:e.size}),null,16,[`size`])]))),128))],2)):t(``,!0)}})})))()}var v;function y(){return(y=e((()=>{_(),f(),v=p(g,[[`__scopeId`,`data-v-afc95a7b`]])})))()}var b,x,S,C,w,T;function E(){return(E=e((()=>{y(),b={title:`Éléments/Génériques/CspMetaList`,component:v,tags:[`autodocs`],parameters:{controls:{include:[`layout`,`size`,`items`]},docs:{description:{component:`Liste de métadonnées avec icône et texte secondaire`}}},argTypes:{layout:{control:{type:`radio`},options:[`inline`,`stacked`],description:`Disposition des métadonnées : en ligne avec retour à la ligne, ou en pile verticale.`,table:{type:{summary:`inline | stacked`},defaultValue:{summary:`inline`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille de la liste : ajuste la taille de texte, l’espacement et la taille des icônes.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},items:{control:{type:`object`},description:`Liste ordonnée des métadonnées à afficher. Chaque item accepte un label visible, une icône Iconify optionnelle et un préfixe réservé aux lecteurs d’écran.`,table:{type:{summary:`CspMetaItem[]`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{layout:`inline`,size:`md`,items:[{srLabel:`Information 1`,label:`Libellé 1`,icon:`ri:calendar-line`},{srLabel:`Information 2`,label:`Libellé 2`,icon:`ri:map-pin-2-line`},{srLabel:`Information 3`,label:`Libellé 3`,icon:`ri:government-line`},{srLabel:`Information 4`,label:`Libellé 4`,icon:`ri:price-tag-3-line`}]},render:e=>({components:{CspMetaList:v},setup(){return{args:e}},template:`<CspMetaList v-bind="args" />`})},x={},S={name:`Sans icônes`,args:{items:[{icon:void 0,srLabel:`Date`,label:`Libellé 1`},{icon:void 0,srLabel:`Canal`,label:`Libellé 2`},{icon:void 0,srLabel:`Audience`,label:`Libellé 3`}]}},C={render:e=>({components:{CspMetaList:v},setup(){return{args:e,sizes:[`sm`,`md`,`lg`]}},template:`
      <div style="display: flex; flex-direction: column; gap: 1rem;">
        <div v-for="size in sizes" :key="size" style="display: flex; flex-direction: column; gap: 0.5rem;">
          <p style="margin: 0; font-size: 0.75rem; color: var(--text-mention-grey);">{{ size }}</p>
          <CspMetaList v-bind="args" :size="size" />
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},w={name:`Disposition empilée`,args:{layout:`stacked`}},x.parameters={...x.parameters,docs:{...x.parameters?.docs,source:{originalSource:`{}`,...x.parameters?.docs?.source}}},S.parameters={...S.parameters,docs:{...S.parameters?.docs,source:{originalSource:`{
  name: 'Sans icônes',
  args: {
    items: [{
      icon: undefined,
      srLabel: 'Date',
      label: 'Libellé 1'
    }, {
      icon: undefined,
      srLabel: 'Canal',
      label: 'Libellé 2'
    }, {
      icon: undefined,
      srLabel: 'Audience',
      label: 'Libellé 3'
    }]
  }
}`,...S.parameters?.docs?.source}}},C.parameters={...C.parameters,docs:{...C.parameters?.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspMetaList
    },
    setup() {
      return {
        args,
        sizes: ['sm', 'md', 'lg']
      };
    },
    template: \`
      <div style="display: flex; flex-direction: column; gap: 1rem;">
        <div v-for="size in sizes" :key="size" style="display: flex; flex-direction: column; gap: 0.5rem;">
          <p style="margin: 0; font-size: 0.75rem; color: var(--text-mention-grey);">{{ size }}</p>
          <CspMetaList v-bind="args" :size="size" />
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...C.parameters?.docs?.source}}},w.parameters={...w.parameters,docs:{...w.parameters?.docs,source:{originalSource:`{
  name: 'Disposition empilée',
  args: {
    layout: 'stacked'
  }
}`,...w.parameters?.docs?.source}}},T=[`Inline`,`WithoutIcons`,`Sizes`,`Stacked`]})))()}E();export{x as Inline,C as Sizes,w as Stacked,S as WithoutIcons,T as __namedExportsOrder,b as default};