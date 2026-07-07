import{i as e}from"./preload-helper-Ct_ODC0V.js";import{Bt as t,D as n,G as r,H as i,K as a,R as o,Ut as s,V as c,W as l,ht as u,lt as d,ot as f,z as p}from"./iframe-z3OQyoHs.js";import{n as m,t as h}from"./_plugin-vue_export-helper-DAS0NJne.js";import{n as g,t as _}from"./CspIcon-DzLi4Zj0.js";var v,y,b,x,S,C,w=e((()=>{n(),g(),v={key:0,class:`csp-callout__icon`},y={class:`csp-callout__content`},b={key:0,class:`csp-callout__title`},x={key:1,class:`csp-callout__description`},S={key:2,class:`csp-callout__body`},C=a({__name:`CspCallout`,props:{variant:{default:`default`},title:{default:null},description:{default:null},icon:{default:null},showIcon:{type:Boolean,default:!0}},setup(e){let n=e,a=u(),m=o(()=>!!a.title||!!n.title),h=o(()=>!!a.description||!!n.description),g=o(()=>!!a.default),C={default:`ri:information-line`,info:`ri:information-line`,success:`ri:checkbox-circle-line`,warning:`ri:alert-line`,error:`ri:error-warning-line`},w=o(()=>n.icon??C[n.variant]);return(n,a)=>(f(),i(`div`,{class:t([`csp-callout`,`csp-callout--${e.variant}`]),role:`alert`},[e.showIcon?(f(),i(`div`,v,[d(n.$slots,`icon`,{},()=>[r(_,{name:w.value},null,8,[`name`])],!0)])):c(``,!0),p(`div`,y,[m.value?(f(),i(`h4`,b,[d(n.$slots,`title`,{},()=>[l(s(e.title),1)],!0)])):c(``,!0),h.value?(f(),i(`p`,x,[d(n.$slots,`description`,{},()=>[l(s(e.description),1)],!0)])):c(``,!0),g.value?(f(),i(`div`,S,[d(n.$slots,`default`,{},void 0,!0)])):c(``,!0)])],2))}})})),T=e((()=>{})),E,D=e((()=>{w(),w(),T(),m(),E=h(C,[[`__scopeId`,`data-v-59f90b3c`]]),C.__docgenInfo=Object.assign({displayName:C.name??C.__name},{exportName:`default`,displayName:`CspCallout`,type:1,props:[{name:`variant`,global:!1,description:``,tags:[],required:!1,type:`"default" | "error" | "info" | "success" | "warning"`,declarations:[],schema:{kind:`enum`,type:`"default" | "error" | "info" | "success" | "warning"`,schema:[`"default"`,`"error"`,`"info"`,`"success"`,`"warning"`]},default:`"default"`},{name:`title`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`null`},{name:`description`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`null`},{name:`icon`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`null`},{name:`showIcon`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`true`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[{name:`icon`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`title`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`description`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[{name:`variant`,type:`"default" | "error" | "info" | "success" | "warning"`,description:``,declarations:[],schema:{kind:`enum`,type:`"default" | "error" | "info" | "success" | "warning"`,schema:[`"default"`,`"error"`,`"info"`,`"success"`,`"warning"`]}},{name:`title`,type:`string`,description:``,declarations:[],schema:`string`},{name:`description`,type:`string`,description:``,declarations:[],schema:`string`},{name:`icon`,type:`string`,description:``,declarations:[],schema:`string`},{name:`showIcon`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspCallout/CspCallout.vue`})})),O,k,A,j,M,N,P,F,I,L,R,z;e((()=>{D(),O={title:`Éléments/Génériques/CspCallout`,component:E,tags:[`autodocs`],parameters:{controls:{include:[`variant`,`title`,`description`,`icon`,`showIcon`]},docs:{description:{component:`Encart d'information pour attirer l'attention de l'utilisateur sur un message important.`}}},argTypes:{variant:{control:{type:`radio`},options:[`default`,`info`,`success`,`warning`,`error`],description:`Variante visuelle du callout.`,table:{type:{summary:`default | info | success | warning | error`},defaultValue:{summary:`default`}}},title:{control:{type:`text`},description:"Titre du callout (ou slot `title`).",table:{type:{summary:`string | null`},defaultValue:{summary:`null`}}},description:{control:{type:`text`},description:"Description du callout (ou slot `description`).",table:{type:{summary:`string | null`},defaultValue:{summary:`null`}}},icon:{control:{type:`text`},description:`Icône personnalisée. Doit être une référence d'icône compatible avec \`CspIcon\` (ex: "ri:lightbulb-line"). Par défaut, l'icône dépend de la variante.`,table:{type:{summary:`string | null`},defaultValue:{summary:`null`}}},showIcon:{control:{type:`boolean`},description:`Affiche ou masque l'icône.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{variant:`default`,title:`Titre du callout`,description:`Description du callout avec des informations complémentaires.`,icon:null,showIcon:!0},render:e=>({components:{CspCallout:E},setup(){return{args:e}},template:`
      <div class="max-w-xl">
        <CspCallout v-bind="args" />
      </div>
    `})},k=[`default`,`info`,`success`,`warning`,`error`],A={},j={args:{title:`Titre du callout sans description`,description:null}},M={args:{variant:`error`,title:`Titre du callout`,description:`Description avec du contenu riche ci-dessous.`},render:e=>({components:{CspCallout:E},setup(){return{args:e}},template:`
      <div class="max-w-xl">
        <CspCallout v-bind="args">
          <ul>
            <li>Premier élément de la liste</li>
            <li>Deuxième élément de la liste</li>
            <li>Troisième élément de la liste</li>
          </ul>
        </CspCallout>
      </div>
    `})},N={render:e=>({components:{CspCallout:E},setup(){return{variants:k,args:e}},template:`
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
    `})},P={args:{variant:`info`,title:`Titre du callout`,description:`Description du callout avec une icône personnalisée.`,icon:`ri:lightbulb-line`}},F={args:{title:`Titre du callout`,description:`Description du callout sans icône.`,showIcon:!1}},I={args:{variant:`success`,title:`Titre du callout`,description:`Description du callout avec la variante success.`}},L={args:{variant:`warning`,title:`Titre du callout`,description:`Description du callout avec la variante warning.`}},R={args:{variant:`error`,title:`Titre du callout`,description:`Description du callout avec la variante error.`}},A.parameters={...A.parameters,docs:{...A.parameters?.docs,source:{originalSource:`{}`,...A.parameters?.docs?.source}}},j.parameters={...j.parameters,docs:{...j.parameters?.docs,source:{originalSource:`{
  args: {
    title: 'Titre du callout sans description',
    description: null
  }
}`,...j.parameters?.docs?.source}}},M.parameters={...M.parameters,docs:{...M.parameters?.docs,source:{originalSource:`{
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
}`,...M.parameters?.docs?.source}}},N.parameters={...N.parameters,docs:{...N.parameters?.docs,source:{originalSource:`{
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
}`,...N.parameters?.docs?.source}}},P.parameters={...P.parameters,docs:{...P.parameters?.docs,source:{originalSource:`{
  args: {
    variant: 'info',
    title: 'Titre du callout',
    description: 'Description du callout avec une icône personnalisée.',
    icon: 'ri:lightbulb-line'
  }
}`,...P.parameters?.docs?.source}}},F.parameters={...F.parameters,docs:{...F.parameters?.docs,source:{originalSource:`{
  args: {
    title: 'Titre du callout',
    description: 'Description du callout sans icône.',
    showIcon: false
  }
}`,...F.parameters?.docs?.source}}},I.parameters={...I.parameters,docs:{...I.parameters?.docs,source:{originalSource:`{
  args: {
    variant: 'success',
    title: 'Titre du callout',
    description: 'Description du callout avec la variante success.'
  }
}`,...I.parameters?.docs?.source}}},L.parameters={...L.parameters,docs:{...L.parameters?.docs,source:{originalSource:`{
  args: {
    variant: 'warning',
    title: 'Titre du callout',
    description: 'Description du callout avec la variante warning.'
  }
}`,...L.parameters?.docs?.source}}},R.parameters={...R.parameters,docs:{...R.parameters?.docs,source:{originalSource:`{
  args: {
    variant: 'error',
    title: 'Titre du callout',
    description: 'Description du callout avec la variante error.'
  }
}`,...R.parameters?.docs?.source}}},z=[`Default`,`TitleOnly`,`WithRichContent`,`Variants`,`WithCustomIcon`,`WithoutIcon`,`Success`,`Warning`,`Error`]}))();export{A as Default,R as Error,I as Success,j as TitleOnly,N as Variants,L as Warning,P as WithCustomIcon,M as WithRichContent,F as WithoutIcon,z as __namedExportsOrder,O as default};