import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{C as t,E as n,F as r,H as i,O as a,Ot as o,S as s,Tt as c,X as l,Z as u,c as d,h as f,ht as p,it as m,m as h,p as g,w as _,x as v}from"./iframe-jcHRdFNq.js";import{n as y,t as b}from"./CspIcon-CCw9Ulm0.js";import{n as x,t as S}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{n as C,t as w}from"./CspButton-CNa5Z0OQ.js";var T,E,D,O,k,A,j;function M(){return(M=e((()=>{d(),C(),y(),T=[`for`],E={key:0,class:`csp-search-bar__hint`},D={class:`csp-search-bar__field`},O=[`id`,`name`,`placeholder`,`disabled`,`aria-invalid`,`aria-describedby`,`onKeydown`],k=[`id`],A={key:0,class:`csp-search-bar__error`},j=a({__name:`CspSearchBar`,props:r({label:{},mode:{default:`submit`},hideLabel:{type:Boolean,default:!1},hint:{},placeholder:{},size:{default:`md`},disabled:{type:Boolean,default:!1},error:{type:Boolean,default:!1},errorMessage:{},buttonLabel:{default:`Rechercher`},id:{default:()=>l()},name:{}},{modelValue:{default:``},modelModifiers:{}}),emits:r([`search`],[`update:modelValue`]),setup(e,{emit:r}){let a=e,l=r,d=u(e,`modelValue`);function p(){a.disabled||l(`search`,d.value.trim())}return(r,a)=>(i(),_(`div`,{class:c([`csp-search-bar`,[`csp-search-bar--${e.size}`,`csp-search-bar--${e.mode}`,{"csp-search-bar--error":e.error}]]),role:`search`},[v(`label`,{class:c([`csp-search-bar__label`,{"csp-search-bar__label--hidden":e.hideLabel}]),for:e.id},[n(o(e.label)+` `,1),e.hint?(i(),_(`span`,E,o(e.hint),1)):t(``,!0)],10,T),v(`div`,D,[e.mode===`live`?(i(),s(b,{key:0,name:`ri:search-line`,class:`csp-search-bar__icon`,"aria-hidden":`true`})):t(``,!0),m(v(`input`,{id:e.id,"onUpdate:modelValue":a[0]||=e=>d.value=e,class:`csp-search-bar__input`,type:`search`,name:e.name,placeholder:e.placeholder,disabled:e.disabled,"aria-invalid":e.error||void 0,"aria-describedby":`${e.id}-messages`,autocomplete:`off`,onKeydown:h(f(p,[`prevent`]),[`enter`])},null,40,O),[[g,d.value]]),e.mode===`submit`&&e.size===`lg`?(i(),s(w,{key:1,class:`csp-search-bar__button`,label:e.buttonLabel,icon:`ri:search-line`,"is-icon-left":``,disabled:e.disabled,onClick:p},null,8,[`label`,`disabled`])):e.mode===`submit`?(i(),s(w,{key:2,class:`csp-search-bar__button`,icon:`ri:search-line`,"aria-label":e.buttonLabel,title:e.buttonLabel,disabled:e.disabled,onClick:p},null,8,[`aria-label`,`title`,`disabled`])):t(``,!0)]),v(`div`,{id:`${e.id}-messages`,class:`csp-search-bar__messages`,"aria-live":`polite`},[e.error&&e.errorMessage?(i(),_(`p`,A,o(e.errorMessage),1)):t(``,!0)],8,k)],2))}})})))()}var N;function P(){return(P=e((()=>{M(),x(),N=S(j,[[`__scopeId`,`data-v-97e16b2d`]])})))()}function F(e){return{components:{CspSearchBar:N},setup(){return{args:e,value:p(``),submitted:p(``)}},template:`
      <div style="max-width: 32rem;">
        <CspSearchBar v-bind="args" v-model="value" @search="submitted = $event" />
        <p v-if="submitted" style="margin-top: 1rem; font-size: 0.875rem; color: var(--text-mention-grey);">Recherche lancée : {{ submitted }}</p>
      </div>
    `}}var I,L,R,z,B,V,H,U,W;function G(){return(G=e((()=>{d(),P(),I={title:`Éléments/Génériques/CspSearchBar`,component:N,tags:[`autodocs`],parameters:{controls:{include:[`label`,`mode`,`hideLabel`,`hint`,`placeholder`,`size`,`disabled`,`error`,`errorMessage`,`buttonLabel`]},docs:{description:{component:"Barre de recherche DSFR, en deux modes. En mode `submit`, par défaut, la recherche se lance à la validation : un bouton accompagne le champ, et l’événement `search` porte la valeur sans espaces superflus au clic ou à la touche Entrée. En mode `live`, la recherche suit la saisie par le `v-model` : le bouton disparaît et une loupe discrète signale le champ de recherche. La touche Entrée émet toujours `search`, pour appliquer un filtre qui attend une pause dans la frappe. Le libellé peut être masqué visuellement dans une barre d’outils, il reste le nom accessible du champ. Deux tailles : MD pour une recherche contextuelle, LG pour un moteur mis en avant."}}},argTypes:{mode:{control:`radio`,options:[`submit`,`live`]},size:{control:`radio`,options:[`md`,`lg`]}},args:{label:`Rechercher`,placeholder:`Rechercher`,size:`md`}},L={render:F},R={name:`Filtre au fil de la saisie`,args:{mode:`live`,hideLabel:!0,placeholder:`Filtrer la liste`},render:F},z={args:{size:`lg`},render:F},B={name:`Libellé masqué`,args:{hideLabel:!0},render:F},V={name:`Avec indication`,args:{label:`Adresse email`,hint:`Adresse complète du compte`,placeholder:`prenom.nom@exemple.gouv.fr`},render:F},H={args:{error:!0,errorMessage:`Aucun résultat pour cette recherche.`},render:F},U={args:{disabled:!0},render:F},L.parameters={...L.parameters,docs:{...L.parameters?.docs,source:{originalSource:`{
  render
}`,...L.parameters?.docs?.source}}},R.parameters={...R.parameters,docs:{...R.parameters?.docs,source:{originalSource:`{
  name: 'Filtre au fil de la saisie',
  args: {
    mode: 'live',
    hideLabel: true,
    placeholder: 'Filtrer la liste'
  },
  render
}`,...R.parameters?.docs?.source}}},z.parameters={...z.parameters,docs:{...z.parameters?.docs,source:{originalSource:`{
  args: {
    size: 'lg'
  },
  render
}`,...z.parameters?.docs?.source}}},B.parameters={...B.parameters,docs:{...B.parameters?.docs,source:{originalSource:`{
  name: 'Libellé masqué',
  args: {
    hideLabel: true
  },
  render
}`,...B.parameters?.docs?.source}}},V.parameters={...V.parameters,docs:{...V.parameters?.docs,source:{originalSource:`{
  name: 'Avec indication',
  args: {
    label: 'Adresse email',
    hint: 'Adresse complète du compte',
    placeholder: 'prenom.nom@exemple.gouv.fr'
  },
  render
}`,...V.parameters?.docs?.source}}},H.parameters={...H.parameters,docs:{...H.parameters?.docs,source:{originalSource:`{
  args: {
    error: true,
    errorMessage: 'Aucun résultat pour cette recherche.'
  },
  render
}`,...H.parameters?.docs?.source}}},U.parameters={...U.parameters,docs:{...U.parameters?.docs,source:{originalSource:`{
  args: {
    disabled: true
  },
  render
}`,...U.parameters?.docs?.source}}},W=[`Default`,`Live`,`Large`,`HiddenLabel`,`WithHint`,`Error`,`Disabled`]})))()}G();export{L as Default,U as Disabled,H as Error,B as HiddenLabel,z as Large,R as Live,V as WithHint,W as __namedExportsOrder,I as default};