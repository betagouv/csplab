import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{C as t,D as n,Dt as r,E as i,S as a,T as o,V as s,W as c,Z as l,b as u,c as d,wt as f,y as p}from"./iframe-CZzSM9_p.js";import{n as m,t as h}from"./CspIcon-D7bFwQs9.js";import{n as g,t as _}from"./_plugin-vue_export-helper-BqBa3wPr.js";var v,y,b,x,S,C;function w(){return(w=e((()=>{d(),m(),v={key:0,class:`csp-callout__icon`},y={class:`csp-callout__content`},b={key:0,class:`csp-callout__title`},x={key:1,class:`csp-callout__description`},S={key:2,class:`csp-callout__body`},C=n({__name:`CspCallout`,props:{variant:{default:`default`},title:{default:null},description:{default:null},icon:{default:null},showIcon:{type:Boolean,default:!0}},setup(e){let n=e,d=l(),m=p(()=>!!d.title||!!n.title),g=p(()=>!!d.description||!!n.description),_=p(()=>!!d.default),C={default:`ri:information-line`,info:`ri:information-line`,success:`ri:checkbox-circle-line`,warning:`ri:alert-line`,error:`ri:error-warning-line`},w=p(()=>n.icon??C[n.variant]);return(n,l)=>(s(),t(`div`,{class:f([`csp-callout`,`csp-callout--${e.variant}`]),role:`alert`},[e.showIcon?(s(),t(`div`,v,[c(n.$slots,`icon`,{},()=>[i(h,{name:w.value},null,8,[`name`])],!0)])):a(``,!0),u(`div`,y,[m.value?(s(),t(`h4`,b,[c(n.$slots,`title`,{},()=>[o(r(e.title),1)],!0)])):a(``,!0),g.value?(s(),t(`p`,x,[c(n.$slots,`description`,{},()=>[o(r(e.description),1)],!0)])):a(``,!0),_.value?(s(),t(`div`,S,[c(n.$slots,`default`,{},void 0,!0)])):a(``,!0)])],2))}})})))()}var T;function E(){return(E=e((()=>{w(),g(),T=_(C,[[`__scopeId`,`data-v-59f90b3c`]])})))()}var D,O,k,A,j,M,N,P,F,I,L,R;function z(){return(z=e((()=>{E(),D={title:`Éléments/Génériques/CspCallout`,component:T,tags:[`autodocs`],parameters:{controls:{include:[`variant`,`title`,`description`,`icon`,`showIcon`]},docs:{description:{component:`Encart d'information pour attirer l'attention de l'utilisateur sur un message important.`}}},argTypes:{variant:{control:{type:`radio`},options:[`default`,`info`,`success`,`warning`,`error`],description:`Variante visuelle du callout.`,table:{type:{summary:`default | info | success | warning | error`},defaultValue:{summary:`default`}}},title:{control:{type:`text`},description:"Titre du callout (ou slot `title`).",table:{type:{summary:`string | null`},defaultValue:{summary:`null`}}},description:{control:{type:`text`},description:"Description du callout (ou slot `description`).",table:{type:{summary:`string | null`},defaultValue:{summary:`null`}}},icon:{control:{type:`text`},description:`Icône personnalisée. Doit être une référence d'icône compatible avec \`CspIcon\` (ex: "ri:lightbulb-line"). Par défaut, l'icône dépend de la variante.`,table:{type:{summary:`string | null`},defaultValue:{summary:`null`}}},showIcon:{control:{type:`boolean`},description:`Affiche ou masque l'icône.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{variant:`default`,title:`Titre du callout`,description:`Description du callout avec des informations complémentaires.`,icon:null,showIcon:!0},render:e=>({components:{CspCallout:T},setup(){return{args:e}},template:`
      <div class="max-w-xl">
        <CspCallout v-bind="args" />
      </div>
    `})},O=[`default`,`info`,`success`,`warning`,`error`],k={},A={args:{title:`Titre du callout sans description`,description:null}},j={args:{variant:`error`,title:`Titre du callout`,description:`Description avec du contenu riche ci-dessous.`},render:e=>({components:{CspCallout:T},setup(){return{args:e}},template:`
      <div class="max-w-xl">
        <CspCallout v-bind="args">
          <ul>
            <li>Premier élément de la liste</li>
            <li>Deuxième élément de la liste</li>
            <li>Troisième élément de la liste</li>
          </ul>
        </CspCallout>
      </div>
    `})},M={render:e=>({components:{CspCallout:T},setup(){return{variants:O,args:e}},template:`
      <div class="flex flex-col gap-4 max-w-xl">
        <CspCallout
          v-for="v in variants"
          :key="v"
          v-bind="args"
          :variant="v"
          :title="'Titre du callout (' + v + ')'"
          description="Description du callout avec des informations complémentaires."
        />
      </div>
    `})},N={args:{variant:`info`,title:`Titre du callout`,description:`Description du callout avec une icône personnalisée.`,icon:`ri:lightbulb-line`}},P={args:{title:`Titre du callout`,description:`Description du callout sans icône.`,showIcon:!1}},F={args:{variant:`success`,title:`Titre du callout`,description:`Description du callout avec la variante success.`}},I={args:{variant:`warning`,title:`Titre du callout`,description:`Description du callout avec la variante warning.`}},L={args:{variant:`error`,title:`Titre du callout`,description:`Description du callout avec la variante error.`}},k.parameters={...k.parameters,docs:{...k.parameters?.docs,source:{originalSource:`{}`,...k.parameters?.docs?.source}}},A.parameters={...A.parameters,docs:{...A.parameters?.docs,source:{originalSource:`{
  args: {
    title: 'Titre du callout sans description',
    description: null
  }
}`,...A.parameters?.docs?.source}}},j.parameters={...j.parameters,docs:{...j.parameters?.docs,source:{originalSource:`{
  args: {
    variant: 'error',
    title: 'Titre du callout',
    description: 'Description avec du contenu riche ci-dessous.'
  },
  render: args => ({
    components: {
      CspCallout
    },
    setup() {
      return {
        args
      };
    },
    template: \`
      <div class="max-w-xl">
        <CspCallout v-bind="args">
          <ul>
            <li>Premier élément de la liste</li>
            <li>Deuxième élément de la liste</li>
            <li>Troisième élément de la liste</li>
          </ul>
        </CspCallout>
      </div>
    \`
  })
}`,...j.parameters?.docs?.source}}},M.parameters={...M.parameters,docs:{...M.parameters?.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspCallout
    },
    setup() {
      return {
        variants: VARIANTS,
        args
      };
    },
    template: \`
      <div class="flex flex-col gap-4 max-w-xl">
        <CspCallout
          v-for="v in variants"
          :key="v"
          v-bind="args"
          :variant="v"
          :title="'Titre du callout (' + v + ')'"
          description="Description du callout avec des informations complémentaires."
        />
      </div>
    \`
  })
}`,...M.parameters?.docs?.source}}},N.parameters={...N.parameters,docs:{...N.parameters?.docs,source:{originalSource:`{
  args: {
    variant: 'info',
    title: 'Titre du callout',
    description: 'Description du callout avec une icône personnalisée.',
    icon: 'ri:lightbulb-line'
  }
}`,...N.parameters?.docs?.source}}},P.parameters={...P.parameters,docs:{...P.parameters?.docs,source:{originalSource:`{
  args: {
    title: 'Titre du callout',
    description: 'Description du callout sans icône.',
    showIcon: false
  }
}`,...P.parameters?.docs?.source}}},F.parameters={...F.parameters,docs:{...F.parameters?.docs,source:{originalSource:`{
  args: {
    variant: 'success',
    title: 'Titre du callout',
    description: 'Description du callout avec la variante success.'
  }
}`,...F.parameters?.docs?.source}}},I.parameters={...I.parameters,docs:{...I.parameters?.docs,source:{originalSource:`{
  args: {
    variant: 'warning',
    title: 'Titre du callout',
    description: 'Description du callout avec la variante warning.'
  }
}`,...I.parameters?.docs?.source}}},L.parameters={...L.parameters,docs:{...L.parameters?.docs,source:{originalSource:`{
  args: {
    variant: 'error',
    title: 'Titre du callout',
    description: 'Description du callout avec la variante error.'
  }
}`,...L.parameters?.docs?.source}}},R=[`Default`,`TitleOnly`,`WithRichContent`,`Variants`,`WithCustomIcon`,`WithoutIcon`,`Success`,`Warning`,`Error`]})))()}z();export{k as Default,L as Error,F as Success,A as TitleOnly,M as Variants,I as Warning,N as WithCustomIcon,j as WithRichContent,P as WithoutIcon,R as __namedExportsOrder,D as default};