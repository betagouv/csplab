import{i as e}from"./preload-helper-Ct_ODC0V.js";import{D as t,H as n,Ht as r,K as i,ot as a}from"./iframe-DahxzZvw.js";import{n as o,t as s}from"./_plugin-vue_export-helper-DAS0NJne.js";var c,l=e((()=>{t(),c=i({__name:`CspSkeleton`,props:{width:{default:`100%`},height:{default:`1rem`}},setup(e){return(t,i)=>(a(),n(`span`,{class:`csp-skeleton`,style:r({width:e.width,height:e.height}),"aria-hidden":`true`},null,4))}})})),u=e((()=>{})),d,f=e((()=>{l(),l(),u(),o(),d=s(c,[[`__scopeId`,`data-v-16e357cb`]]),c.__docgenInfo=Object.assign({displayName:c.name??c.__name},{exportName:`default`,displayName:`CspSkeleton`,type:1,props:[{name:`width`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`"100%"`},{name:`height`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`"1rem"`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[],exposed:[{name:`width`,type:`string`,description:``,declarations:[],schema:`string`},{name:`height`,type:`string`,description:``,declarations:[],schema:`string`}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspSkeleton/CspSkeleton.vue`})})),p,m,h,g;e((()=>{f(),p={title:`Éléments/Génériques/CspSkeleton`,component:d,tags:[`autodocs`],parameters:{controls:{include:[`width`,`height`]},docs:{description:{component:`Bloc de chargement neutre qui réserve l'espace du contenu à venir, pour éviter les décalages de mise en page (layout shift). Dimensionner au plus proche du contenu final.`}}},argTypes:{width:{control:{type:`text`},description:`Largeur CSS du bloc.`,table:{type:{summary:`string`},defaultValue:{summary:`100%`}}},height:{control:{type:`text`},description:`Hauteur CSS du bloc.`,table:{type:{summary:`string`},defaultValue:{summary:`1rem`}}}}},m={name:`Par défaut`,args:{width:`16rem`,height:`1rem`}},h={name:`Titre et métadonnées`,render:()=>({components:{CspSkeleton:d},template:`
      <div style="display: flex; flex-direction: column; gap: 0.5rem;">
        <CspSkeleton width="20rem" height="2rem" />
        <CspSkeleton width="28rem" height="1.375rem" />
      </div>
    `})},m.parameters={...m.parameters,docs:{...m.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut',
  args: {
    width: '16rem',
    height: '1rem'
  }
}`,...m.parameters?.docs?.source}}},h.parameters={...h.parameters,docs:{...h.parameters?.docs,source:{originalSource:`{
  name: 'Titre et métadonnées',
  render: () => ({
    components: {
      CspSkeleton
    },
    template: \`
      <div style="display: flex; flex-direction: column; gap: 0.5rem;">
        <CspSkeleton width="20rem" height="2rem" />
        <CspSkeleton width="28rem" height="1.375rem" />
      </div>
    \`
  })
}`,...h.parameters?.docs?.source}}},g=[`Default`,`TitleAndMeta`]}))();export{m as Default,h as TitleAndMeta,g as __namedExportsOrder,p as default};