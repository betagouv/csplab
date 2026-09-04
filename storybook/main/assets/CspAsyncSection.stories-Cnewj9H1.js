import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{Dt as t,G as n,H as r,O as i,S as a,T as o,Tt as s,c,rt as l,w as u}from"./iframe-kccjvU-D.js";import{n as d,t as f}from"./CspErrorState-BuNc0BQZ.js";import{n as p,t as m}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{n as h,t as g}from"./CspSkeletonTable-DslYe8lJ.js";var _,v;function y(){return(y=e((()=>{c(),d(),_=[`aria-label`],v=i({__name:`CspAsyncSection`,props:{pending:{type:Boolean},error:{default:void 0},loadingLabel:{default:`Chargement`},errorTitle:{default:void 0},errorDescription:{default:void 0},fill:{type:Boolean,default:!1},minHeight:{default:void 0}},setup(e){return(i,c)=>(r(),u(`div`,{class:s([`csp-async-section`,{"csp-async-section--fill":e.fill}]),style:t(e.minHeight?{minHeight:e.minHeight}:void 0)},[e.pending?(r(),u(`div`,{key:0,class:`csp-async-section__loading`,role:`status`,"aria-label":e.loadingLabel},[n(i.$slots,`skeleton`,{},void 0,!0)],8,_)):e.error?(r(),a(f,{key:1,title:e.errorTitle,description:e.errorDescription},o({_:2},[i.$slots[`error-action`]?{name:`action`,fn:l(()=>[n(i.$slots,`error-action`,{},void 0,!0)]),key:`0`}:void 0]),1032,[`title`,`description`])):n(i.$slots,`default`,{},void 0,!0,2)],6))}})})))()}var b;function x(){return(x=e((()=>{y(),p(),b=m(v,[[`__scopeId`,`data-v-815a79cd`]])})))()}function S(e){return{components:{CspAsyncSection:b,CspSkeletonTable:g},setup(){return{args:e}},template:`
      <CspAsyncSection v-bind="args">
        <template #skeleton>
          <CspSkeletonTable :rows="4" :columns="3" />
        </template>
        <p>Contenu chargé.</p>
      </CspAsyncSection>
    `}}var C,w,T,E,D;function O(){return(O=e((()=>{x(),h(),C={title:`Compositions/Génériques/CspAsyncSection`,component:b,tags:[`autodocs`],parameters:{controls:{include:[`pending`,`errorTitle`,`loadingLabel`,`minHeight`]},docs:{description:{component:`Section asynchrone : orchestre le contrat skeleton (pending) → CspErrorState (error) → contenu, avec zone de chargement accessible (role="status") et hauteur réservable.`}}}},w={args:{pending:!0,loadingLabel:`Chargement des données`},render:S},T={args:{pending:!1,error:!0,errorTitle:`Une erreur est survenue lors du chargement.`,minHeight:`16rem`},render:S},E={args:{pending:!1},render:S},w.parameters={...w.parameters,docs:{...w.parameters?.docs,source:{originalSource:`{
  args: {
    pending: true,
    loadingLabel: 'Chargement des données'
  },
  render: renderSection
}`,...w.parameters?.docs?.source}}},T.parameters={...T.parameters,docs:{...T.parameters?.docs,source:{originalSource:`{
  args: {
    pending: false,
    error: true,
    errorTitle: 'Une erreur est survenue lors du chargement.',
    minHeight: '16rem'
  },
  render: renderSection
}`,...T.parameters?.docs?.source}}},E.parameters={...E.parameters,docs:{...E.parameters?.docs,source:{originalSource:`{
  args: {
    pending: false
  },
  render: renderSection
}`,...E.parameters?.docs?.source}}},D=[`Chargement`,`Erreur`,`Contenu`]})))()}O();export{w as Chargement,E as Contenu,T as Erreur,D as __namedExportsOrder,C as default};