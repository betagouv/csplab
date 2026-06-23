import{i as e}from"./preload-helper-DXs2ar-j.js";import{B as t,C as n,F as r,I as i,L as a,Mt as o,P as s,R as c,Rt as l,Tt as u,V as d,Y as f,dt as p,it as m,mt as h,st as g,tt as _,ut as v,z as y}from"./iframe-VMof5POA.js";import{A as b,E as x,M as S,O as C,P as w,S as T,b as E,t as D,w as O}from"./dist-DUxhYj4V.js";import{n as k,t as A}from"./CspIcon-BwuARc0E.js";import{n as j,t as M}from"./CspButton-CvmtirB5.js";var N,P,F,I,L,R,z=e((()=>{n(),D(),j(),k(),N={class:`csp-toast__layout`},P={key:0,class:`csp-toast__icon`},F={class:`csp-toast__content`},I={key:2,class:`csp-toast__body`},L={key:1,class:`csp-toast__actions`},R=d({inheritAttrs:!1,__name:`CspToast`,props:{open:{type:Boolean,default:void 0},defaultOpen:{type:Boolean,default:!1},title:{default:null},description:{default:null},duration:{default:void 0},variant:{default:`default`},showIcon:{type:Boolean,default:!0},actionLabel:{default:null},actionAltText:{default:`Exécuter l'action`},showClose:{type:Boolean,default:!0},closeLabel:{default:`Fermer la notification`}},emits:[`update:open`,`action`],setup(e,{emit:n}){let u=e,d=n,p=g(),x=v(),w=s(()=>!!x.title||!!u.title),E=s(()=>!!x.description||!!u.description),D=s(()=>!!x.action||!!u.actionLabel),k={default:`ri:notification-3-line`,info:`ri:information-line`,success:`ri:checkbox-circle-line`,warning:`ri:alert-line`,error:`ri:error-warning-line`},j=s(()=>k[u.variant]);return(n,s)=>(_(),i(o(O),f(o(p),{open:e.open,"default-open":e.defaultOpen,duration:e.duration,class:[`csp-toast`,`csp-toast--${e.variant}`],"onUpdate:open":s[1]||=e=>d(`update:open`,e)}),{default:h(()=>[r(`div`,N,[e.showIcon?(_(),c(`div`,P,[m(n.$slots,`icon`,{},()=>[t(A,{name:j.value},null,8,[`name`])])])):a(``,!0),r(`div`,F,[w.value?(_(),i(o(T),{key:0,as:`h3`,class:`csp-toast__title`},{default:h(()=>[m(n.$slots,`title`,{},()=>[y(l(e.title),1)])]),_:3})):a(``,!0),E.value?(_(),i(o(C),{key:1,as:`p`,class:`csp-toast__description`},{default:h(()=>[m(n.$slots,`description`,{},()=>[y(l(e.description),1)])]),_:3})):a(``,!0),n.$slots.default?(_(),c(`div`,I,[m(n.$slots,`default`)])):a(``,!0)]),D.value||e.showClose?(_(),c(`div`,L,[D.value?(_(),i(o(b),{key:0,"as-child":``,"alt-text":e.actionAltText,onClick:s[0]||=e=>d(`action`)},{default:h(()=>[m(n.$slots,`action`,{},()=>[t(M,{variant:`tertiary-no-outline`,size:`sm`,label:e.actionLabel},null,8,[`label`])])]),_:3},8,[`alt-text`])):a(``,!0),e.showClose?(_(),i(o(S),{key:1,"as-child":``},{default:h(()=>[t(M,{variant:`tertiary-no-outline`,size:`sm`,icon:`ri:close-line`,"aria-label":e.closeLabel},null,8,[`aria-label`])]),_:1})):a(``,!0)])):a(``,!0)])]),_:3},16,[`open`,`default-open`,`duration`,`class`]))}})})),B=e((()=>{})),V,H=e((()=>{z(),z(),B(),V=R,R.__docgenInfo=Object.assign({displayName:R.name??R.__name},{exportName:`default`,displayName:`CspToast`,type:1,props:[{name:`variant`,global:!1,description:``,tags:[],required:!1,type:`"default" | "error" | "info" | "success" | "warning"`,declarations:[],schema:{kind:`enum`,type:`"default" | "error" | "info" | "success" | "warning"`,schema:[`"default"`,`"error"`,`"info"`,`"success"`,`"warning"`]},default:`"default"`},{name:`open`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`undefined`},{name:`defaultOpen`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`title`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`null`},{name:`description`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`null`},{name:`duration`,global:!1,description:``,tags:[],required:!1,type:`number`,declarations:[],schema:`number`,default:`undefined`},{name:`showIcon`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`true`},{name:`actionLabel`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`null`},{name:`actionAltText`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`"Ex\\u00E9cuter l'action"`},{name:`showClose`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`true`},{name:`closeLabel`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`"Fermer la notification"`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[{name:`update:open`,description:``,tags:[],type:`[value: boolean]`,signature:`(event: "update:open", value: boolean): void`,declarations:[],schema:[{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}]},{name:`action`,description:``,tags:[],type:`[]`,signature:`(event: "action"): void`,declarations:[],schema:[]}],slots:[{name:`icon`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`title`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`description`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`action`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[{name:`$slots`,type:`Readonly<InternalSlots> & { icon?: (props: {}) => any; } & { title?: (props: {}) => any; } & { description?: (props: {}) => any; } & { default?: (props: {}) => any; } & { ...; }`,description:``,declarations:[],schema:{kind:`object`,type:`Readonly<InternalSlots> & { icon?: (props: {}) => any; } & { title?: (props: {}) => any; } & { description?: (props: {}) => any; } & { default?: (props: {}) => any; } & { ...; }`}},{name:`variant`,type:`"default" | "error" | "info" | "success" | "warning"`,description:``,declarations:[],schema:{kind:`enum`,type:`"default" | "error" | "info" | "success" | "warning"`,schema:[`"default"`,`"error"`,`"info"`,`"success"`,`"warning"`]}},{name:`open`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`defaultOpen`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`title`,type:`string`,description:``,declarations:[],schema:`string`},{name:`description`,type:`string`,description:``,declarations:[],schema:`string`},{name:`duration`,type:`number`,description:``,declarations:[],schema:`number`},{name:`showIcon`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`actionLabel`,type:`string`,description:``,declarations:[],schema:`string`},{name:`actionAltText`,type:`string`,description:``,declarations:[],schema:`string`},{name:`showClose`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`closeLabel`,type:`string`,description:``,declarations:[],schema:`string`}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspToast/CspToast.vue`})})),U,W=e((()=>{n(),D(),U=d({__name:`CspToastProvider`,props:{label:{default:`Notification`},duration:{default:3200},swipeDirection:{default:`right`},disableSwipe:{type:Boolean,default:!1}},setup(e){return(n,r)=>(_(),i(o(w),{label:e.label,duration:e.duration,"disable-swipe":e.disableSwipe,"swipe-direction":e.swipeDirection},{default:h(()=>[m(n.$slots,`default`),t(o(x),null,{default:h(()=>[t(o(E),{class:`csp-toast-viewport`})]),_:1})]),_:3},8,[`label`,`duration`,`disable-swipe`,`swipe-direction`]))}})})),G=e((()=>{})),K,q=e((()=>{W(),W(),G(),K=U,U.__docgenInfo=Object.assign({displayName:U.name??U.__name},{exportName:`default`,displayName:`CspToastProvider`,type:1,props:[{name:`label`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`"Notification"`},{name:`duration`,global:!1,description:``,tags:[],required:!1,type:`number`,declarations:[],schema:`number`,default:`3200`},{name:`swipeDirection`,global:!1,description:``,tags:[],required:!1,type:`"right" | "left" | "up" | "down"`,declarations:[],schema:{kind:`enum`,type:`"right" | "left" | "up" | "down"`,schema:[`"right"`,`"left"`,`"up"`,`"down"`]},default:`"right"`},{name:`disableSwipe`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[{name:`label`,type:`string`,description:``,declarations:[],schema:`string`},{name:`duration`,type:`number`,description:``,declarations:[],schema:`number`},{name:`swipeDirection`,type:`"right" | "left" | "up" | "down"`,description:``,declarations:[],schema:{kind:`enum`,type:`"right" | "left" | "up" | "down"`,schema:[`"right"`,`"left"`,`"up"`,`"down"`]}},{name:`disableSwipe`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspToast/CspToastProvider.vue`})})),J,Y,X,Z,Q;e((()=>{n(),j(),H(),q(),J={title:`Éléments/Génériques/CspToast`,component:V,tags:[`autodocs`],parameters:{controls:{include:[`open`,`defaultOpen`,`title`,`description`,`duration`,`variant`,`showIcon`,`actionLabel`,`actionAltText`,`showClose`,`closeLabel`]},docs:{description:{component:`Notification toast accessible basée sur reka-ui. Doit être utilisé à l'intérieur d'un unique CspToastProvider placé à la racine de l'app.`}}},argTypes:{open:{control:{type:`boolean`},description:"État d'ouverture contrôlé. Liez avec `v-model:open`.",table:{type:{summary:`boolean`}}},defaultOpen:{control:{type:`boolean`},description:`État d'ouverture initial en mode non contrôlé.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},title:{control:{type:`text`},description:"Titre du toast (ou slot `title`).",table:{type:{summary:`string | null`}}},description:{control:{type:`text`},description:"Description du toast (ou slot `description`).",table:{type:{summary:`string | null`}}},duration:{control:{type:`number`},description:`Durée d'affichage en millisecondes. Hérite du provider si non défini.`,table:{type:{summary:`number`}}},variant:{control:{type:`radio`},options:[`default`,`info`,`success`,`warning`,`error`],description:`Variante visuelle de la notification.`,table:{type:{summary:`default | info | success | warning | error`},defaultValue:{summary:`default`}}},showIcon:{control:{type:`boolean`},description:`Affiche ou masque l'icone.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},actionLabel:{control:{type:`text`},description:`Label du bouton d'action.`,table:{type:{summary:`string | null`}}},actionAltText:{control:{type:`text`},description:`Texte alternatif annoncé pour l'action.`,table:{type:{summary:`string`},defaultValue:{summary:`Exécuter l'action`}}},showClose:{control:{type:`boolean`},description:`Affiche ou masque le bouton de fermeture.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},closeLabel:{control:{type:`text`},description:`Libellé accessible du bouton de fermeture.`,table:{type:{summary:`string`},defaultValue:{summary:`Fermer la notification`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{defaultOpen:!1,title:`Action terminée`,description:`Votre modification a bien été enregistrée.`,variant:`success`,showIcon:!0,actionLabel:`Annuler`,actionAltText:`Annuler la dernière action`,showClose:!0,closeLabel:`Fermer la notification`},render:e=>({components:{CspButton:M,CspToast:V,CspToastProvider:K},setup(){let t=u(!!e.open);p(()=>e.open,e=>{e!==void 0&&(t.value=e)});function n(){t.value=!0}function r(e){t.value=e}return{args:e,open:t,showToast:n,handleUpdateOpen:r}},template:`
      <CspToastProvider>
        <CspButton
          label="Afficher le toast"
          variant="primary"
          @click="showToast"
        />

        <CspToast
          v-bind="args"
          :open="args.open === undefined ? open : args.open"
          @update:open="handleUpdateOpen"
        />
      </CspToastProvider>
    `})},Y={},X={render:e=>({components:{CspButton:M,CspToast:V,CspToastProvider:K},setup(){let t=[`default`,`info`,`success`,`warning`,`error`],n=u(!1),r=u(`default`);function i(e){r.value=e,n.value=!0}function a(e){n.value=e}return{args:e,variants:t,open:n,currentVariant:r,openVariant:i,updateOpen:a}},template:`
      <CspToastProvider>
        <div class="flex flex-wrap gap-3">
          <CspButton
            v-for="variant in variants"
            :key="variant"
            :label="'Toast ' + variant"
            variant="secondary"
            @click="openVariant(variant)"
          />
        </div>

        <CspToast
          v-bind="args"
          :open="open"
          :variant="currentVariant"
          :title="'Notification ' + currentVariant"
          :description="'Exemple pour la variante ' + currentVariant + '.'"
          @update:open="updateOpen"
        />
      </CspToastProvider>
    `})},Z={render:()=>({components:{CspButton:M,CspToast:V,CspToastProvider:K},setup(){let e=u([]),t=0;function n(n){e.value.push({id:t++,variant:n,title:`Notification ${n} #${t}`})}function r(t){e.value=e.value.filter(e=>e.id!==t)}return{toasts:e,addToast:n,removeToast:r}},template:`
      <CspToastProvider :duration="4000">
        <div class="flex flex-wrap gap-3">
          <CspButton label="Info" variant="secondary" @click="addToast('info')" />
          <CspButton label="Success" variant="secondary" @click="addToast('success')" />
          <CspButton label="Warning" variant="secondary" @click="addToast('warning')" />
          <CspButton label="Error" variant="secondary" @click="addToast('error')" />
        </div>

        <CspToast
          v-for="toast in toasts"
          :key="toast.id"
          :open="true"
          :variant="toast.variant"
          :title="toast.title"
          description="Cette notification fonctionne avec les autres."
          :show-close="true"
          @update:open="(v) => !v && removeToast(toast.id)"
        />
      </CspToastProvider>
    `})},Y.parameters={...Y.parameters,docs:{...Y.parameters?.docs,source:{originalSource:`{}`,...Y.parameters?.docs?.source}}},X.parameters={...X.parameters,docs:{...X.parameters?.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspButton,
      CspToast,
      CspToastProvider
    },
    setup() {
      const variants = ['default', 'info', 'success', 'warning', 'error'] as const;
      const open = ref(false);
      const currentVariant = ref<(typeof variants)[number]>('default');
      function openVariant(variant: (typeof variants)[number]) {
        currentVariant.value = variant;
        open.value = true;
      }
      function updateOpen(value: boolean) {
        open.value = value;
      }
      return {
        args,
        variants,
        open,
        currentVariant,
        openVariant,
        updateOpen
      };
    },
    template: \`
      <CspToastProvider>
        <div class="flex flex-wrap gap-3">
          <CspButton
            v-for="variant in variants"
            :key="variant"
            :label="'Toast ' + variant"
            variant="secondary"
            @click="openVariant(variant)"
          />
        </div>

        <CspToast
          v-bind="args"
          :open="open"
          :variant="currentVariant"
          :title="'Notification ' + currentVariant"
          :description="'Exemple pour la variante ' + currentVariant + '.'"
          @update:open="updateOpen"
        />
      </CspToastProvider>
    \`
  })
}`,...X.parameters?.docs?.source}}},Z.parameters={...Z.parameters,docs:{...Z.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspButton,
      CspToast,
      CspToastProvider
    },
    setup() {
      const toasts = ref<Array<{
        id: number;
        variant: 'info' | 'success' | 'warning' | 'error';
        title: string;
      }>>([]);
      let nextId = 0;
      function addToast(variant: 'info' | 'success' | 'warning' | 'error') {
        toasts.value.push({
          id: nextId++,
          variant,
          title: \`Notification \${variant} #\${nextId}\`
        });
      }
      function removeToast(id: number) {
        toasts.value = toasts.value.filter(t => t.id !== id);
      }
      return {
        toasts,
        addToast,
        removeToast
      };
    },
    template: \`
      <CspToastProvider :duration="4000">
        <div class="flex flex-wrap gap-3">
          <CspButton label="Info" variant="secondary" @click="addToast('info')" />
          <CspButton label="Success" variant="secondary" @click="addToast('success')" />
          <CspButton label="Warning" variant="secondary" @click="addToast('warning')" />
          <CspButton label="Error" variant="secondary" @click="addToast('error')" />
        </div>

        <CspToast
          v-for="toast in toasts"
          :key="toast.id"
          :open="true"
          :variant="toast.variant"
          :title="toast.title"
          description="Cette notification fonctionne avec les autres."
          :show-close="true"
          @update:open="(v) => !v && removeToast(toast.id)"
        />
      </CspToastProvider>
    \`
  })
}`,...Z.parameters?.docs?.source}}},Q=[`Default`,`Variants`,`MultipleToasts`]}))();export{Y as Default,Z as MultipleToasts,X as Variants,Q as __namedExportsOrder,J as default};