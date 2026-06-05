import{C as G}from"./CspButton-h93eUcVJ.js";import{k as Y,W as ee,f as v,Z as _,v as te,K as S,b as a,E as t,h as l,J as i,g as s,i as C,N as b}from"./vue.esm-bundler-aFrwtEYQ.js";import{_ as ae}from"./CspIcon-BtBbcwlP.js";import{_ as se}from"./_plugin-vue_export-helper-DlAUqK2U.js";import"./iconify-LI3XAFZD.js";const re={key:0,class:"csp-card__start"},ne={key:1,class:"csp-card__header"},le=["href"],ie={key:1,class:"csp-card__description"},oe={key:2,class:"csp-card__body"},de={key:3,class:"csp-card__end"},ce={key:4,class:"csp-card__footer"},H=Y({__name:"CspCard",props:{as:{default:"article"},variant:{default:"default"},size:{default:"md"},title:{default:null},titleAs:{default:"h3"},description:{default:null},href:{}},setup(e){const g=e,o=ee(),k=a(()=>!!o.title||!!g.title),x=a(()=>!!o.description||!!g.description),J=a(()=>k.value||x.value),M=a(()=>!!o.start),Q=a(()=>!!o.default),U=a(()=>!!o.end),X=a(()=>!!o.footer),h=a(()=>!!g.href);return(n,ue)=>(t(),v(S(e.as),{class:te(["csp-card",[`csp-card--${e.variant}`,`csp-card--${e.size}`,{"csp-card--link":h.value}]])},{default:_(()=>[M.value?(t(),l("div",re,[i(n.$slots,"start",{},void 0,!0)])):s("",!0),J.value?(t(),l("header",ne,[k.value?(t(),v(S(e.titleAs),{key:0,class:"csp-card__title"},{default:_(()=>[h.value?(t(),l("a",{key:0,href:e.href,class:"csp-card__link"},[i(n.$slots,"title",{},()=>[C(b(e.title),1)],!0)],8,le)):i(n.$slots,"title",{key:1},()=>[C(b(e.title),1)],!0)]),_:3})):s("",!0),x.value?(t(),l("p",ie,[i(n.$slots,"description",{},()=>[C(b(e.description),1)],!0)])):s("",!0)])):s("",!0),Q.value?(t(),l("div",oe,[i(n.$slots,"default",{},void 0,!0)])):s("",!0),U.value?(t(),l("div",de,[i(n.$slots,"end",{},void 0,!0)])):s("",!0),X.value?(t(),l("footer",ce,[i(n.$slots,"footer",{},void 0,!0)])):s("",!0),h.value?(t(),v(ae,{key:5,name:"ri:arrow-right-line",class:"csp-card__arrow",size:20})):s("",!0)]),_:3},8,["class"]))}}),r=se(H,[["__scopeId","data-v-12b33683"]]);H.__docgenInfo={exportName:"default",displayName:"CspCard",type:1,props:[{name:"size",global:!1,description:"",tags:[],required:!1,type:'"md" | "sm" | "lg"',declarations:[],schema:{kind:"enum",type:'"md" | "sm" | "lg"',schema:['"md"','"sm"','"lg"']},default:'"md"'},{name:"variant",global:!1,description:"",tags:[],required:!1,type:'"default" | "alt"',declarations:[],schema:{kind:"enum",type:'"default" | "alt"',schema:['"default"','"alt"']},default:'"default"'},{name:"as",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string",default:'"article"'},{name:"title",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string",default:"null"},{name:"description",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string",default:"null"},{name:"titleAs",global:!1,description:"",tags:[],required:!1,type:'"h2" | "h3" | "h4" | "h5" | "h6"',declarations:[],schema:{kind:"enum",type:'"h2" | "h3" | "h4" | "h5" | "h6"',schema:['"h2"','"h3"','"h4"','"h5"','"h6"']},default:'"h3"'},{name:"key",global:!0,description:"",tags:[],required:!1,type:"PropertyKey",declarations:[],schema:{kind:"enum",type:"PropertyKey",schema:["string","number","symbol"]}},{name:"ref",global:!0,description:"",tags:[],required:!1,type:"VNodeRef",declarations:[],schema:{kind:"enum",type:"VNodeRef",schema:["string","Ref<any, any>",{kind:"event",type:"(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void"}]}},{name:"ref_for",global:!0,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"ref_key",global:!0,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"class",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"},{name:"style",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"},{name:"href",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"}],events:[],slots:[{name:"start",type:"{}",description:"",declarations:[],schema:{kind:"object",type:"{}"}},{name:"title",type:"{}",description:"",declarations:[],schema:{kind:"object",type:"{}"}},{name:"description",type:"{}",description:"",declarations:[],schema:{kind:"object",type:"{}"}},{name:"default",type:"{}",description:"",declarations:[],schema:{kind:"object",type:"{}"}},{name:"end",type:"{}",description:"",declarations:[],schema:{kind:"object",type:"{}"}},{name:"footer",type:"{}",description:"",declarations:[],schema:{kind:"object",type:"{}"}}],exposed:[{name:"$slots",type:"Readonly<InternalSlots> & { start?: (props: {}) => any; } & { title?: (props: {}) => any; } & { title?: (props: {}) => any; } & { description?: (props: {}) => any; } & { ...; } & { ...; } & { ...; }",description:"",declarations:[],schema:{kind:"object",type:"Readonly<InternalSlots> & { start?: (props: {}) => any; } & { title?: (props: {}) => any; } & { title?: (props: {}) => any; } & { description?: (props: {}) => any; } & { ...; } & { ...; } & { ...; }"}},{name:"size",type:'"md" | "sm" | "lg"',description:"",declarations:[],schema:{kind:"enum",type:'"md" | "sm" | "lg"',schema:['"md"','"sm"','"lg"']}},{name:"variant",type:'"default" | "alt"',description:"",declarations:[],schema:{kind:"enum",type:'"default" | "alt"',schema:['"default"','"alt"']}},{name:"as",type:"string",description:"",declarations:[],schema:"string"},{name:"title",type:"string",description:"",declarations:[],schema:"string"},{name:"description",type:"string",description:"",declarations:[],schema:"string"},{name:"titleAs",type:'"h2" | "h3" | "h4" | "h5" | "h6"',description:"",declarations:[],schema:{kind:"enum",type:'"h2" | "h3" | "h4" | "h5" | "h6"',schema:['"h2"','"h3"','"h4"','"h5"','"h6"']}},{name:"href",type:"string",description:"",declarations:[],schema:"string"}],sourceFiles:"/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspCard/CspCard.vue"};const Ce={title:"Éléments/Génériques/CspCard",component:r,tags:["autodocs"],parameters:{controls:{include:["variant","size","as","title","titleAs","description","href"]},docs:{description:{component:"Carte générique pour présenter du contenu avec un titre, une description et des actions associées."}}},argTypes:{variant:{control:{type:"radio"},options:["default","alt"],description:"Style visuel.",table:{type:{summary:"default | alt"},defaultValue:{summary:"default"}}},size:{control:{type:"radio"},options:["sm","md","lg"],description:"Taille de la carte : ajuste padding, interlignes et typographie.",table:{type:{summary:"sm | md | lg"},defaultValue:{summary:"md"}}},as:{control:{type:"radio"},options:["article","section","div"],description:"Élément racine rendu.",table:{type:{summary:"string"},defaultValue:{summary:"article"}}},title:{control:{type:"text"},description:"Titre de la carte. Surclassé par le slot `title`.",table:{type:{summary:"string | null"},defaultValue:{summary:"null"}}},titleAs:{control:{type:"radio"},options:["h2","h3","h4","h5","h6"],description:"Niveau de titre rendu (accessibilité).",table:{type:{summary:"h2 | h3 | h4 | h5 | h6"},defaultValue:{summary:"h3"}}},description:{control:{type:"text"},description:"Description de la carte. Surclassée par le slot `description`.",table:{type:{summary:"string | null"},defaultValue:{summary:"null"}}},href:{control:{type:"text"},description:"Active le motif « carte cliquable » : le titre devient un lien couvrant toute la carte.",table:{type:{summary:"string"}}},default:{control:!1,table:{disable:!0}},start:{control:!1,table:{disable:!0}},end:{control:!1,table:{disable:!0}},footer:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{variant:"default",size:"md",as:"article",title:"Titre de la carte",titleAs:"h3",description:"Description courte qui précise le contenu de la carte.",href:void 0},render:e=>({components:{CspButton:G,CspCard:r},setup(){return{args:e}},template:`
      <div class="max-w-xl">
        <CspCard v-bind="args">
          <p>Contenu principal de la carte, placé dans le slot par défaut.</p>

          <template #footer>
            <CspButton label="Action" variant="primary" />
            <CspButton label="Secondaire" variant="secondary" />
          </template>
        </CspCard>
      </div>
    `})},pe=["default","alt"],me=["sm","md","lg"],d={},c={render:e=>({components:{CspCard:r},setup(){return{args:e}},template:`
      <div class="max-w-xl">
        <CspCard v-bind="args" />
      </div>
    `})},p={args:{title:"Libellé du lien",description:"Description courte de la carte cliquable.",href:"#"},render:e=>({components:{CspCard:r},setup(){return{args:e}},template:`
      <div class="max-w-xl">
        <CspCard v-bind="args">
          <p>La carte entière est cliquable : titre bleu et flèche signalent l'interactivité.</p>
        </CspCard>
      </div>
    `})},m={render:e=>({components:{CspCard:r},setup(){return{args:e}},template:`
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
    `})},u={render:e=>({components:{CspButton:G,CspCard:r},setup(){return{args:e}},template:`
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
    `})},f={render:e=>({components:{CspCard:r},setup(){return{variants:pe,args:e}},template:`
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
    `})},y={render:e=>({components:{CspCard:r},setup(){return{sizes:me,args:e}},template:`
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
    `})};var B,w,q;d.parameters={...d.parameters,docs:{...(B=d.parameters)==null?void 0:B.docs,source:{originalSource:"{}",...(q=(w=d.parameters)==null?void 0:w.docs)==null?void 0:q.source}}};var z,A,T;c.parameters={...c.parameters,docs:{...(z=c.parameters)==null?void 0:z.docs,source:{originalSource:`{
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
}`,...(T=(A=c.parameters)==null?void 0:A.docs)==null?void 0:T.source}}};var P,V,D;p.parameters={...p.parameters,docs:{...(P=p.parameters)==null?void 0:P.docs,source:{originalSource:`{
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
}`,...(D=(V=p.parameters)==null?void 0:V.docs)==null?void 0:D.source}}};var I,$,N;m.parameters={...m.parameters,docs:{...(I=m.parameters)==null?void 0:I.docs,source:{originalSource:`{
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
}`,...(N=($=m.parameters)==null?void 0:$.docs)==null?void 0:N.source}}};var E,L,j;u.parameters={...u.parameters,docs:{...(E=u.parameters)==null?void 0:E.docs,source:{originalSource:`{
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
}`,...(j=(L=u.parameters)==null?void 0:L.docs)==null?void 0:j.source}}};var R,W,K;f.parameters={...f.parameters,docs:{...(R=f.parameters)==null?void 0:R.docs,source:{originalSource:`{
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
}`,...(K=(W=f.parameters)==null?void 0:W.docs)==null?void 0:K.source}}};var O,Z,F;y.parameters={...y.parameters,docs:{...(O=y.parameters)==null?void 0:O.docs,source:{originalSource:`{
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
}`,...(F=(Z=y.parameters)==null?void 0:Z.docs)==null?void 0:F.source}}};const be=["Default","TitleAndDescription","WithLink","WithStartAndEnd","Composition","Variants","Sizes"];export{u as Composition,d as Default,y as Sizes,c as TitleAndDescription,f as Variants,p as WithLink,m as WithStartAndEnd,be as __namedExportsOrder,Ce as default};
