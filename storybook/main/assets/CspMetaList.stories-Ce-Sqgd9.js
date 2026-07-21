import{i as e}from"./preload-helper-Ct_ODC0V.js";import{Bt as t,D as n,F as r,G as i,H as a,K as o,R as s,V as c,ct as l,et as u,ot as d}from"./iframe-Cw6ThQzZ.js";import{n as f,t as p}from"./_plugin-vue_export-helper-DAS0NJne.js";import{n as m,t as h}from"./CspMeta-C3Wgh3QY.js";var g,_=e((()=>{n(),m(),g=o({__name:`CspMetaList`,props:{items:{},size:{default:`md`},layout:{default:`inline`}},setup(e){let n=e,o=s(()=>[`csp-meta-list`,`csp-meta-list--${n.layout}`,`csp-meta-list--${n.size}`]);return(n,s)=>e.items.length?(d(),a(`ul`,{key:0,class:t(o.value)},[(d(!0),a(r,null,l(e.items,(t,n)=>(d(),a(`li`,{key:`${t.label}-${n}`,class:`csp-meta-list__item`},[i(h,u({ref_for:!0},t,{size:e.size}),null,16,[`size`])]))),128))],2)):c(``,!0)}})})),v=e((()=>{})),y,b=e((()=>{_(),_(),v(),f(),y=p(g,[[`__scopeId`,`data-v-7c84360e`]]),g.__docgenInfo=Object.assign({displayName:g.name??g.__name},{exportName:`default`,displayName:`CspMetaList`,type:1,props:[{name:`items`,global:!1,description:``,tags:[],required:!0,type:`CspMetaItem[]`,declarations:[],schema:{kind:`array`,type:`CspMetaItem[]`}},{name:`size`,global:!1,description:``,tags:[],required:!1,type:`"md" | "sm" | "lg"`,declarations:[],schema:{kind:`enum`,type:`"md" | "sm" | "lg"`,schema:[`"md"`,`"sm"`,`"lg"`]},default:`"md"`},{name:`layout`,global:!1,description:``,tags:[],required:!1,type:`"inline" | "stacked"`,declarations:[],schema:{kind:`enum`,type:`"inline" | "stacked"`,schema:[`"inline"`,`"stacked"`]},default:`"inline"`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[],exposed:[{name:`size`,type:`"md" | "sm" | "lg"`,description:``,declarations:[],schema:{kind:`enum`,type:`"md" | "sm" | "lg"`,schema:[`"md"`,`"sm"`,`"lg"`]}},{name:`layout`,type:`"inline" | "stacked"`,description:``,declarations:[],schema:{kind:`enum`,type:`"inline" | "stacked"`,schema:[`"inline"`,`"stacked"`]}},{name:`items`,type:`CspMetaItem[]`,description:``,declarations:[],schema:{kind:`array`,type:`CspMetaItem[]`}}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspMeta/CspMetaList.vue`})})),x,S,C,w,T,E;e((()=>{b(),x={title:`Éléments/Génériques/CspMetaList`,component:y,tags:[`autodocs`],parameters:{controls:{include:[`layout`,`size`,`items`]},docs:{description:{component:`Liste de métadonnées avec icône et texte secondaire`}}},argTypes:{layout:{control:{type:`radio`},options:[`inline`,`stacked`],description:`Disposition des métadonnées : en ligne avec retour à la ligne, ou en pile verticale.`,table:{type:{summary:`inline | stacked`},defaultValue:{summary:`inline`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille de la liste : ajuste la taille de texte, l’espacement et la taille des icônes.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},items:{control:{type:`object`},description:`Liste ordonnée des métadonnées à afficher. Chaque item accepte un label visible, une icône Iconify optionnelle et un préfixe réservé aux lecteurs d’écran.`,table:{type:{summary:`CspMetaItem[]`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{layout:`inline`,size:`md`,items:[{srLabel:`Information 1`,label:`Libellé 1`,icon:`ri:calendar-line`},{srLabel:`Information 2`,label:`Libellé 2`,icon:`ri:map-pin-2-line`},{srLabel:`Information 3`,label:`Libellé 3`,icon:`ri:government-line`},{srLabel:`Information 4`,label:`Libellé 4`,icon:`ri:price-tag-3-line`}]},render:e=>({components:{CspMetaList:y},setup(){return{args:e}},template:`<CspMetaList v-bind="args" />`})},S={},C={name:`Sans icônes`,args:{items:[{icon:void 0,srLabel:`Date`,label:`Libellé 1`},{icon:void 0,srLabel:`Canal`,label:`Libellé 2`},{icon:void 0,srLabel:`Audience`,label:`Libellé 3`}]}},w={render:e=>({components:{CspMetaList:y},setup(){return{args:e,sizes:[`sm`,`md`,`lg`]}},template:`
      <div style="display: flex; flex-direction: column; gap: 1rem;">
        <div v-for="size in sizes" :key="size" style="display: flex; flex-direction: column; gap: 0.5rem;">
          <p style="margin: 0; font-size: 0.75rem; color: var(--text-mention-grey);">{{ size }}</p>
          <CspMetaList v-bind="args" :size="size" />
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},T={name:`Disposition empilée`,args:{layout:`stacked`}},S.parameters={...S.parameters,docs:{...S.parameters?.docs,source:{originalSource:`{}`,...S.parameters?.docs?.source}}},C.parameters={...C.parameters,docs:{...C.parameters?.docs,source:{originalSource:`{
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
}`,...C.parameters?.docs?.source}}},w.parameters={...w.parameters,docs:{...w.parameters?.docs,source:{originalSource:`{
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
}`,...w.parameters?.docs?.source}}},T.parameters={...T.parameters,docs:{...T.parameters?.docs,source:{originalSource:`{
  name: 'Disposition empilée',
  args: {
    layout: 'stacked'
  }
}`,...T.parameters?.docs?.source}}},E=[`Inline`,`WithoutIcons`,`Sizes`,`Stacked`]}))();export{S as Inline,w as Sizes,T as Stacked,C as WithoutIcons,E as __namedExportsOrder,x as default};