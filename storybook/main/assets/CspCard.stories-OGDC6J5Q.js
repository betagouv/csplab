import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{C as t,D as n,Dt as r,K as i,S as a,T as o,V as s,W as c,Z as l,c as u,nt as d,wt as f,x as p,y as m}from"./iframe-2MukLbfH.js";import{n as h,t as g}from"./CspIcon-xGkUiU-7.js";import{n as _,t as v}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{n as y,t as b}from"./CspButton-C8t1GQ-6.js";var x,S,C,w,T,E,D,O;function k(){return(k=e((()=>{u(),h(),x={key:0,class:`csp-card__start`},S={key:1,class:`csp-card__header`},C=[`href`],w={key:1,class:`csp-card__description`},T={key:2,class:`csp-card__body`},E={key:3,class:`csp-card__end`},D={key:4,class:`csp-card__footer`},O=n({__name:`CspCard`,props:{as:{default:`article`},variant:{default:`default`},size:{default:`md`},title:{default:null},titleAs:{default:`h3`},description:{default:null},href:{}},setup(e){let n=e,u=l(),h=m(()=>!!u.title||!!n.title),_=m(()=>!!u.description||!!n.description),v=m(()=>h.value||_.value),y=m(()=>!!u.start),b=m(()=>!!u.default),O=m(()=>!!u.end),k=m(()=>!!u.footer),A=m(()=>!!n.href);return(n,l)=>(s(),p(i(e.as),{class:f([`csp-card`,[`csp-card--${e.variant}`,`csp-card--${e.size}`,{"csp-card--link":A.value}]])},{default:d(()=>[y.value?(s(),t(`div`,x,[c(n.$slots,`start`,{},void 0,!0)])):a(``,!0),v.value?(s(),t(`header`,S,[h.value?(s(),p(i(e.titleAs),{key:0,class:`csp-card__title`},{default:d(()=>[A.value?(s(),t(`a`,{key:0,href:e.href,class:`csp-card__link`},[c(n.$slots,`title`,{},()=>[o(r(e.title),1)],!0)],8,C)):c(n.$slots,`title`,{},()=>[o(r(e.title),1)],!0,1)]),_:3})):a(``,!0),_.value?(s(),t(`p`,w,[c(n.$slots,`description`,{},()=>[o(r(e.description),1)],!0)])):a(``,!0)])):a(``,!0),b.value?(s(),t(`div`,T,[c(n.$slots,`default`,{},void 0,!0)])):a(``,!0),O.value?(s(),t(`div`,E,[c(n.$slots,`end`,{},void 0,!0)])):a(``,!0),k.value?(s(),t(`footer`,D,[c(n.$slots,`footer`,{},void 0,!0)])):a(``,!0),A.value?(s(),p(g,{key:5,name:`ri:arrow-right-line`,class:`csp-card__arrow`,size:20})):a(``,!0)]),_:3},8,[`class`]))}})})))()}var A;function j(){return(j=e((()=>{k(),_(),A=v(O,[[`__scopeId`,`data-v-12b33683`]])})))()}var M,N,P,F,I,L,R,z,B,V,H;function U(){return(U=e((()=>{y(),j(),M={title:`Éléments/Génériques/CspCard`,component:A,tags:[`autodocs`],parameters:{controls:{include:[`variant`,`size`,`as`,`title`,`titleAs`,`description`,`href`]},docs:{description:{component:`Carte générique pour présenter du contenu avec un titre, une description et des actions associées.`}}},argTypes:{variant:{control:{type:`radio`},options:[`default`,`alt`],description:`Style visuel.`,table:{type:{summary:`default | alt`},defaultValue:{summary:`default`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille de la carte : ajuste padding, interlignes et typographie.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},as:{control:{type:`radio`},options:[`article`,`section`,`div`],description:`Élément racine rendu.`,table:{type:{summary:`string`},defaultValue:{summary:`article`}}},title:{control:{type:`text`},description:"Titre de la carte. Surclassé par le slot `title`.",table:{type:{summary:`string | null`},defaultValue:{summary:`null`}}},titleAs:{control:{type:`radio`},options:[`h2`,`h3`,`h4`,`h5`,`h6`],description:`Niveau de titre rendu (accessibilité).`,table:{type:{summary:`h2 | h3 | h4 | h5 | h6`},defaultValue:{summary:`h3`}}},description:{control:{type:`text`},description:"Description de la carte. Surclassée par le slot `description`.",table:{type:{summary:`string | null`},defaultValue:{summary:`null`}}},href:{control:{type:`text`},description:`Active le motif « carte cliquable » : le titre devient un lien couvrant toute la carte.`,table:{type:{summary:`string`}}},default:{control:!1,table:{disable:!0}},start:{control:!1,table:{disable:!0}},end:{control:!1,table:{disable:!0}},footer:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{variant:`default`,size:`md`,as:`article`,title:`Titre de la carte`,titleAs:`h3`,description:`Description courte qui précise le contenu de la carte.`,href:void 0},render:e=>({components:{CspButton:b,CspCard:A},setup(){return{args:e}},template:`
      <div class="max-w-xl">
        <CspCard v-bind="args">
          <p>Contenu principal de la carte, placé dans le slot par défaut.</p>

          <template #footer>
            <CspButton label="Action" variant="primary" />
            <CspButton label="Secondaire" variant="secondary" />
          </template>
        </CspCard>
      </div>
    `})},N=[`default`,`alt`],P=[`sm`,`md`,`lg`],F={},I={render:e=>({components:{CspCard:A},setup(){return{args:e}},template:`
      <div class="max-w-xl">
        <CspCard v-bind="args" />
      </div>
    `})},L={args:{title:`Libellé du lien`,description:`Description courte de la carte cliquable.`,href:`#`},render:e=>({components:{CspCard:A},setup(){return{args:e}},template:`
      <div class="max-w-xl">
        <CspCard v-bind="args">
          <p>La carte entière est cliquable : titre bleu et flèche signalent l'interactivité.</p>
        </CspCard>
      </div>
    `})},R={render:e=>({components:{CspCard:A},setup(){return{args:e}},template:`
      <div class="max-w-xl">
        <CspCard v-bind="args">
          <template #start>
            <!-- Placeholder : remplacer par de futurs CspTag / CspBadge -->
            <span class="csp-card-story-placeholder">Tag</span>
            <span class="csp-card-story-placeholder">Badge</span>
          </template>

          <p>Corps de la carte décrivant le contenu principal.</p>

          <template #end>
            <!-- Placeholder : informations méta (date, lieu, durée…) -->
            <span>Information méta</span>
          </template>
        </CspCard>
      </div>

      <style>
        .csp-card-story-placeholder {
          display: inline-flex;
          align-items: center;
          padding: 0.125rem 0.5rem;
          border-radius: 0.25rem;
          font-size: 0.75rem;
          background-color: var(--background-alt-blue-france);
          color: var(--text-action-high-blue-france);
        }
      </style>
    `})},z={render:e=>({components:{CspButton:b,CspCard:A},setup(){return{args:e}},template:`
      <div class="max-w-xl">
        <CspCard v-bind="args" :title="null" :description="null">
          <template #title>
            Titre via slot
          </template>
          <template #description>
            Description via slot, pouvant contenir du <strong>balisage</strong>.
          </template>

          <p>Corps de la carte libre.</p>

          <template #footer>
            <CspButton label="Libellé" variant="primary" />
          </template>
        </CspCard>
      </div>
    `})},B={render:e=>({components:{CspCard:A},setup(){return{variants:N,args:e}},template:`
      <div class="flex flex-col gap-6 max-w-xl">
        <CspCard
          v-for="v in variants"
          :key="v"
          v-bind="args"
          :variant="v"
          :title="v"
          description="Contenu de démonstration."
        />
      </div>
    `})},V={render:e=>({components:{CspCard:A},setup(){return{sizes:P,args:e}},template:`
      <div class="flex flex-col gap-6 max-w-xl">
        <CspCard
          v-for="s in sizes"
          :key="s"
          v-bind="args"
          :size="s"
          :title="'size: ' + s"
          description="Contenu de démonstration."
        />
      </div>
    `})},F.parameters={...F.parameters,docs:{...F.parameters?.docs,source:{originalSource:`{}`,...F.parameters?.docs?.source}}},I.parameters={...I.parameters,docs:{...I.parameters?.docs,source:{originalSource:`{
  render: (args: CspCardProps) => ({
    components: {
      CspCard
    },
    setup() {
      return {
        args
      };
    },
    template: \`
      <div class="max-w-xl">
        <CspCard v-bind="args" />
      </div>
    \`
  })
}`,...I.parameters?.docs?.source}}},L.parameters={...L.parameters,docs:{...L.parameters?.docs,source:{originalSource:`{
  args: {
    title: 'Libellé du lien',
    description: 'Description courte de la carte cliquable.',
    href: '#'
  },
  render: (args: CspCardProps) => ({
    components: {
      CspCard
    },
    setup() {
      return {
        args
      };
    },
    template: \`
      <div class="max-w-xl">
        <CspCard v-bind="args">
          <p>La carte entière est cliquable : titre bleu et flèche signalent l'interactivité.</p>
        </CspCard>
      </div>
    \`
  })
}`,...L.parameters?.docs?.source}}},R.parameters={...R.parameters,docs:{...R.parameters?.docs,source:{originalSource:`{
  render: (args: CspCardProps) => ({
    components: {
      CspCard
    },
    setup() {
      return {
        args
      };
    },
    template: \`
      <div class="max-w-xl">
        <CspCard v-bind="args">
          <template #start>
            <!-- Placeholder : remplacer par de futurs CspTag / CspBadge -->
            <span class="csp-card-story-placeholder">Tag</span>
            <span class="csp-card-story-placeholder">Badge</span>
          </template>

          <p>Corps de la carte décrivant le contenu principal.</p>

          <template #end>
            <!-- Placeholder : informations méta (date, lieu, durée…) -->
            <span>Information méta</span>
          </template>
        </CspCard>
      </div>

      <style>
        .csp-card-story-placeholder {
          display: inline-flex;
          align-items: center;
          padding: 0.125rem 0.5rem;
          border-radius: 0.25rem;
          font-size: 0.75rem;
          background-color: var(--background-alt-blue-france);
          color: var(--text-action-high-blue-france);
        }
      </style>
    \`
  })
}`,...R.parameters?.docs?.source}}},z.parameters={...z.parameters,docs:{...z.parameters?.docs,source:{originalSource:`{
  render: (args: CspCardProps) => ({
    components: {
      CspButton,
      CspCard
    },
    setup() {
      return {
        args
      };
    },
    template: \`
      <div class="max-w-xl">
        <CspCard v-bind="args" :title="null" :description="null">
          <template #title>
            Titre via slot
          </template>
          <template #description>
            Description via slot, pouvant contenir du <strong>balisage</strong>.
          </template>

          <p>Corps de la carte libre.</p>

          <template #footer>
            <CspButton label="Libellé" variant="primary" />
          </template>
        </CspCard>
      </div>
    \`
  })
}`,...z.parameters?.docs?.source}}},B.parameters={...B.parameters,docs:{...B.parameters?.docs,source:{originalSource:`{
  render: (args: CspCardProps) => ({
    components: {
      CspCard
    },
    setup() {
      return {
        variants: VARIANTS,
        args
      };
    },
    template: \`
      <div class="flex flex-col gap-6 max-w-xl">
        <CspCard
          v-for="v in variants"
          :key="v"
          v-bind="args"
          :variant="v"
          :title="v"
          description="Contenu de démonstration."
        />
      </div>
    \`
  })
}`,...B.parameters?.docs?.source}}},V.parameters={...V.parameters,docs:{...V.parameters?.docs,source:{originalSource:`{
  render: (args: CspCardProps) => ({
    components: {
      CspCard
    },
    setup() {
      return {
        sizes: SIZES,
        args
      };
    },
    template: \`
      <div class="flex flex-col gap-6 max-w-xl">
        <CspCard
          v-for="s in sizes"
          :key="s"
          v-bind="args"
          :size="s"
          :title="'size: ' + s"
          description="Contenu de démonstration."
        />
      </div>
    \`
  })
}`,...V.parameters?.docs?.source}}},H=[`Default`,`TitleAndDescription`,`WithLink`,`WithStartAndEnd`,`Composition`,`Variants`,`Sizes`]})))()}U();export{z as Composition,F as Default,V as Sizes,I as TitleAndDescription,B as Variants,L as WithLink,R as WithStartAndEnd,H as __namedExportsOrder,M as default};