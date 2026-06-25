import{i as e}from"./preload-helper-DXs2ar-j.js";import{B as t,D as n,G as r,H as i,Ht as a,R as o,U as s,V as c,at as l,ct as u,lt as d,mt as f,vt as p,zt as m}from"./iframe-mX1irY5K.js";import{n as h,t as g}from"./_plugin-vue_export-helper-BWZZ3XGR.js";import{n as _,t as v}from"./CspIcon-DCwx8tQv.js";import{n as y,t as b}from"./CspButton-BeMIEgOu.js";var x,S,C,w,T,E,D,O,k=e((()=>{n(),_(),x={key:0,class:`csp-card__start`},S={key:1,class:`csp-card__header`},C=[`href`],w={key:1,class:`csp-card__description`},T={key:2,class:`csp-card__body`},E={key:3,class:`csp-card__end`},D={key:4,class:`csp-card__footer`},O=r({__name:`CspCard`,props:{as:{default:`article`},variant:{default:`default`},size:{default:`md`},title:{default:null},titleAs:{default:`h3`},description:{default:null},href:{}},setup(e){let n=e,r=f(),h=o(()=>!!r.title||!!n.title),g=o(()=>!!r.description||!!n.description),_=o(()=>h.value||g.value),y=o(()=>!!r.start),b=o(()=>!!r.default),O=o(()=>!!r.end),k=o(()=>!!r.footer),A=o(()=>!!n.href);return(n,r)=>(l(),t(d(e.as),{class:m([`csp-card`,[`csp-card--${e.variant}`,`csp-card--${e.size}`,{"csp-card--link":A.value}]])},{default:p(()=>[y.value?(l(),i(`div`,x,[u(n.$slots,`start`,{},void 0,!0)])):c(``,!0),_.value?(l(),i(`header`,S,[h.value?(l(),t(d(e.titleAs),{key:0,class:`csp-card__title`},{default:p(()=>[A.value?(l(),i(`a`,{key:0,href:e.href,class:`csp-card__link`},[u(n.$slots,`title`,{},()=>[s(a(e.title),1)],!0)],8,C)):u(n.$slots,`title`,{key:1},()=>[s(a(e.title),1)],!0)]),_:3})):c(``,!0),g.value?(l(),i(`p`,w,[u(n.$slots,`description`,{},()=>[s(a(e.description),1)],!0)])):c(``,!0)])):c(``,!0),b.value?(l(),i(`div`,T,[u(n.$slots,`default`,{},void 0,!0)])):c(``,!0),O.value?(l(),i(`div`,E,[u(n.$slots,`end`,{},void 0,!0)])):c(``,!0),k.value?(l(),i(`footer`,D,[u(n.$slots,`footer`,{},void 0,!0)])):c(``,!0),A.value?(l(),t(v,{key:5,name:`ri:arrow-right-line`,class:`csp-card__arrow`,size:20})):c(``,!0)]),_:3},8,[`class`]))}})})),A=e((()=>{})),j,M=e((()=>{k(),k(),A(),h(),j=g(O,[[`__scopeId`,`data-v-12b33683`]]),O.__docgenInfo=Object.assign({displayName:O.name??O.__name},{exportName:`default`,displayName:`CspCard`,type:1,props:[{name:`size`,global:!1,description:``,tags:[],required:!1,type:`"md" | "sm" | "lg"`,declarations:[],schema:{kind:`enum`,type:`"md" | "sm" | "lg"`,schema:[`"md"`,`"sm"`,`"lg"`]},default:`"md"`},{name:`variant`,global:!1,description:``,tags:[],required:!1,type:`"default" | "alt"`,declarations:[],schema:{kind:`enum`,type:`"default" | "alt"`,schema:[`"default"`,`"alt"`]},default:`"default"`},{name:`as`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`"article"`},{name:`title`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`null`},{name:`description`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`null`},{name:`titleAs`,global:!1,description:``,tags:[],required:!1,type:`"h2" | "h3" | "h4" | "h5" | "h6"`,declarations:[],schema:{kind:`enum`,type:`"h2" | "h3" | "h4" | "h5" | "h6"`,schema:[`"h2"`,`"h3"`,`"h4"`,`"h5"`,`"h6"`]},default:`"h3"`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`href`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`}],events:[],slots:[{name:`start`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`title`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`description`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`end`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`footer`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[{name:`$slots`,type:`Readonly<InternalSlots> & { start?: (props: {}) => any; } & { title?: (props: {}) => any; } & { title?: (props: {}) => any; } & { description?: (props: {}) => any; } & { ...; } & { ...; } & { ...; }`,description:``,declarations:[],schema:{kind:`object`,type:`Readonly<InternalSlots> & { start?: (props: {}) => any; } & { title?: (props: {}) => any; } & { title?: (props: {}) => any; } & { description?: (props: {}) => any; } & { ...; } & { ...; } & { ...; }`}},{name:`size`,type:`"md" | "sm" | "lg"`,description:``,declarations:[],schema:{kind:`enum`,type:`"md" | "sm" | "lg"`,schema:[`"md"`,`"sm"`,`"lg"`]}},{name:`variant`,type:`"default" | "alt"`,description:``,declarations:[],schema:{kind:`enum`,type:`"default" | "alt"`,schema:[`"default"`,`"alt"`]}},{name:`as`,type:`string`,description:``,declarations:[],schema:`string`},{name:`title`,type:`string`,description:``,declarations:[],schema:`string`},{name:`description`,type:`string`,description:``,declarations:[],schema:`string`},{name:`titleAs`,type:`"h2" | "h3" | "h4" | "h5" | "h6"`,description:``,declarations:[],schema:{kind:`enum`,type:`"h2" | "h3" | "h4" | "h5" | "h6"`,schema:[`"h2"`,`"h3"`,`"h4"`,`"h5"`,`"h6"`]}},{name:`href`,type:`string`,description:``,declarations:[],schema:`string`}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspCard/CspCard.vue`})})),N,P,F,I,L,R,z,B,V,H,U;e((()=>{y(),M(),N={title:`Éléments/Génériques/CspCard`,component:j,tags:[`autodocs`],parameters:{controls:{include:[`variant`,`size`,`as`,`title`,`titleAs`,`description`,`href`]},docs:{description:{component:`Carte générique pour présenter du contenu avec un titre, une description et des actions associées.`}}},argTypes:{variant:{control:{type:`radio`},options:[`default`,`alt`],description:`Style visuel.`,table:{type:{summary:`default | alt`},defaultValue:{summary:`default`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille de la carte : ajuste padding, interlignes et typographie.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},as:{control:{type:`radio`},options:[`article`,`section`,`div`],description:`Élément racine rendu.`,table:{type:{summary:`string`},defaultValue:{summary:`article`}}},title:{control:{type:`text`},description:"Titre de la carte. Surclassé par le slot `title`.",table:{type:{summary:`string | null`},defaultValue:{summary:`null`}}},titleAs:{control:{type:`radio`},options:[`h2`,`h3`,`h4`,`h5`,`h6`],description:`Niveau de titre rendu (accessibilité).`,table:{type:{summary:`h2 | h3 | h4 | h5 | h6`},defaultValue:{summary:`h3`}}},description:{control:{type:`text`},description:"Description de la carte. Surclassée par le slot `description`.",table:{type:{summary:`string | null`},defaultValue:{summary:`null`}}},href:{control:{type:`text`},description:`Active le motif « carte cliquable » : le titre devient un lien couvrant toute la carte.`,table:{type:{summary:`string`}}},default:{control:!1,table:{disable:!0}},start:{control:!1,table:{disable:!0}},end:{control:!1,table:{disable:!0}},footer:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{variant:`default`,size:`md`,as:`article`,title:`Titre de la carte`,titleAs:`h3`,description:`Description courte qui précise le contenu de la carte.`,href:void 0},render:e=>({components:{CspButton:b,CspCard:j},setup(){return{args:e}},template:`
      <div class="max-w-xl">
        <CspCard v-bind="args">
          <p>Contenu principal de la carte, placé dans le slot par défaut.</p>

          <template #footer>
            <CspButton label="Action" variant="primary" />
            <CspButton label="Secondaire" variant="secondary" />
          </template>
        </CspCard>
      </div>
    `})},P=[`default`,`alt`],F=[`sm`,`md`,`lg`],I={},L={render:e=>({components:{CspCard:j},setup(){return{args:e}},template:`
      <div class="max-w-xl">
        <CspCard v-bind="args" />
      </div>
    `})},R={args:{title:`Libellé du lien`,description:`Description courte de la carte cliquable.`,href:`#`},render:e=>({components:{CspCard:j},setup(){return{args:e}},template:`
      <div class="max-w-xl">
        <CspCard v-bind="args">
          <p>La carte entière est cliquable : titre bleu et flèche signalent l'interactivité.</p>
        </CspCard>
      </div>
    `})},z={render:e=>({components:{CspCard:j},setup(){return{args:e}},template:`
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
    `})},B={render:e=>({components:{CspButton:b,CspCard:j},setup(){return{args:e}},template:`
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
    `})},V={render:e=>({components:{CspCard:j},setup(){return{variants:P,args:e}},template:`
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
    `})},H={render:e=>({components:{CspCard:j},setup(){return{sizes:F,args:e}},template:`
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
    `})},I.parameters={...I.parameters,docs:{...I.parameters?.docs,source:{originalSource:`{}`,...I.parameters?.docs?.source}}},L.parameters={...L.parameters,docs:{...L.parameters?.docs,source:{originalSource:`{
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
}`,...L.parameters?.docs?.source}}},R.parameters={...R.parameters,docs:{...R.parameters?.docs,source:{originalSource:`{
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
}`,...R.parameters?.docs?.source}}},z.parameters={...z.parameters,docs:{...z.parameters?.docs,source:{originalSource:`{
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
}`,...z.parameters?.docs?.source}}},B.parameters={...B.parameters,docs:{...B.parameters?.docs,source:{originalSource:`{
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
}`,...B.parameters?.docs?.source}}},V.parameters={...V.parameters,docs:{...V.parameters?.docs,source:{originalSource:`{
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
}`,...V.parameters?.docs?.source}}},H.parameters={...H.parameters,docs:{...H.parameters?.docs,source:{originalSource:`{
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
}`,...H.parameters?.docs?.source}}},U=[`Default`,`TitleAndDescription`,`WithLink`,`WithStartAndEnd`,`Composition`,`Variants`,`Sizes`]}))();export{B as Composition,I as Default,H as Sizes,L as TitleAndDescription,V as Variants,R as WithLink,z as WithStartAndEnd,U as __namedExportsOrder,N as default};