import{i as e}from"./preload-helper-DVWsqyFp.js";import{At as t,B as n,D as r,G as i,H as a,K as o,Lt as s,R as c,Ut as l,V as u,W as d,et as f,ft as p,gt as m,ht as h,lt as g,ot as _,yt as v,z as y}from"./iframe-Cav10qEp.js";import{A as b,E as x,M as S,O as C,P as w,S as T,b as E,t as D,w as O}from"./dist-DJiDhsDT.js";import{n as k,t as A}from"./CspIcon-BuV8avr-.js";import{n as j,t as M}from"./CspButton-C1ocScaJ.js";var N,P,F,I,L,R,z=e((()=>{r(),D(),j(),k(),N={class:`csp-toast__layout`},P={key:0,class:`csp-toast__icon`},F={class:`csp-toast__content`},I={key:2,class:`csp-toast__body`},L={key:1,class:`csp-toast__actions`},R=o({inheritAttrs:!1,__name:`CspToast`,props:{open:{type:Boolean,default:void 0},defaultOpen:{type:Boolean,default:!1},title:{default:null},description:{default:null},duration:{default:void 0},variant:{default:`default`},showIcon:{type:Boolean,default:!0},actionLabel:{default:null},actionAltText:{default:`Exécuter l'action`},showClose:{type:Boolean,default:!0},closeLabel:{default:`Fermer la notification`}},emits:[`update:open`,`action`],setup(e,{emit:t}){let r=e,o=t,m=p(),x=h(),w=c(()=>!!x.title||!!r.title),E=c(()=>!!x.description||!!r.description),D=c(()=>!!x.action||!!r.actionLabel),k={default:`ri:notification-3-line`,info:`ri:information-line`,success:`ri:checkbox-circle-line`,warning:`ri:alert-line`,error:`ri:error-warning-line`},j=c(()=>k[r.variant]);return(t,r)=>(_(),n(s(O),f(s(m),{open:e.open,"default-open":e.defaultOpen,duration:e.duration,class:[`csp-toast`,`csp-toast--${e.variant}`],"onUpdate:open":r[1]||=e=>o(`update:open`,e)}),{default:v(()=>[y(`div`,N,[e.showIcon?(_(),a(`div`,P,[g(t.$slots,`icon`,{},()=>[i(A,{name:j.value},null,8,[`name`])])])):u(``,!0),y(`div`,F,[w.value?(_(),n(s(T),{key:0,as:`h3`,class:`csp-toast__title`},{default:v(()=>[g(t.$slots,`title`,{},()=>[d(l(e.title),1)])]),_:3})):u(``,!0),E.value?(_(),n(s(C),{key:1,as:`p`,class:`csp-toast__description`},{default:v(()=>[g(t.$slots,`description`,{},()=>[d(l(e.description),1)])]),_:3})):u(``,!0),t.$slots.default?(_(),a(`div`,I,[g(t.$slots,`default`)])):u(``,!0)]),D.value||e.showClose?(_(),a(`div`,L,[D.value?(_(),n(s(b),{key:0,"as-child":``,"alt-text":e.actionAltText,onClick:r[0]||=e=>o(`action`)},{default:v(()=>[g(t.$slots,`action`,{},()=>[i(M,{variant:`tertiary-no-outline`,size:`sm`,label:e.actionLabel},null,8,[`label`])])]),_:3},8,[`alt-text`])):u(``,!0),e.showClose?(_(),n(s(S),{key:1,"as-child":``},{default:v(()=>[i(M,{variant:`tertiary-no-outline`,size:`sm`,icon:`ri:close-line`,"aria-label":e.closeLabel},null,8,[`aria-label`])]),_:1})):u(``,!0)])):u(``,!0)])]),_:3},16,[`open`,`default-open`,`duration`,`class`]))}})})),B=e((()=>{})),V,H=e((()=>{z(),z(),B(),V=R,R.__docgenInfo=Object.assign({displayName:R.name??R.__name},{exportName:`default`,displayName:`CspToast`,type:1,props:[{name:`variant`,global:!1,description:``,tags:[],required:!1,type:`"default" | "error" | "info" | "warning" | "success"`,declarations:[],schema:{kind:`enum`,type:`"default" | "error" | "info" | "warning" | "success"`,schema:[`"default"`,`"error"`,`"info"`,`"warning"`,`"success"`]},default:`"default"`},{name:`title`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`null`},{name:`description`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`null`},{name:`open`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`undefined`},{name:`defaultOpen`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`showClose`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`true`},{name:`closeLabel`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`"Fermer la notification"`},{name:`duration`,global:!1,description:``,tags:[],required:!1,type:`number`,declarations:[],schema:`number`,default:`undefined`},{name:`showIcon`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`true`},{name:`actionLabel`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`null`},{name:`actionAltText`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`"Ex\\u00E9cuter l'action"`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[{name:`update:open`,description:``,tags:[],type:`[value: boolean]`,signature:`(event: "update:open", value: boolean): void`,declarations:[],schema:[{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}]},{name:`action`,description:``,tags:[],type:`[]`,signature:`(event: "action"): void`,declarations:[],schema:[]}],slots:[{name:`icon`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`title`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`description`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`action`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[{name:`$slots`,type:`Readonly<InternalSlots> & { icon?: (props: {}) => any; } & { title?: (props: {}) => any; } & { description?: (props: {}) => any; } & { default?: (props: {}) => any; } & { ...; }`,description:``,declarations:[],schema:{kind:`object`,type:`Readonly<InternalSlots> & { icon?: (props: {}) => any; } & { title?: (props: {}) => any; } & { description?: (props: {}) => any; } & { default?: (props: {}) => any; } & { ...; }`}},{name:`variant`,type:`"default" | "error" | "info" | "warning" | "success"`,description:``,declarations:[],schema:{kind:`enum`,type:`"default" | "error" | "info" | "warning" | "success"`,schema:[`"default"`,`"error"`,`"info"`,`"warning"`,`"success"`]}},{name:`title`,type:`string`,description:``,declarations:[],schema:`string`},{name:`description`,type:`string`,description:``,declarations:[],schema:`string`},{name:`open`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`defaultOpen`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`showClose`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`closeLabel`,type:`string`,description:``,declarations:[],schema:`string`},{name:`duration`,type:`number`,description:``,declarations:[],schema:`number`},{name:`showIcon`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`actionLabel`,type:`string`,description:``,declarations:[],schema:`string`},{name:`actionAltText`,type:`string`,description:``,declarations:[],schema:`string`}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspToast/CspToast.vue`})})),U,W=e((()=>{r(),D(),U=o({__name:`CspToastProvider`,props:{label:{default:`Notification`},duration:{default:3200},swipeDirection:{default:`right`},disableSwipe:{type:Boolean,default:!1}},setup(e){return(t,r)=>(_(),n(s(w),{label:e.label,duration:e.duration,"disable-swipe":e.disableSwipe,"swipe-direction":e.swipeDirection},{default:v(()=>[g(t.$slots,`default`),i(s(x),null,{default:v(()=>[i(s(E),{class:`csp-toast-viewport`})]),_:1})]),_:3},8,[`label`,`duration`,`disable-swipe`,`swipe-direction`]))}})})),G=e((()=>{})),K,q=e((()=>{W(),W(),G(),K=U,U.__docgenInfo=Object.assign({displayName:U.name??U.__name},{exportName:`default`,displayName:`CspToastProvider`,type:1,props:[{name:`label`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`"Notification"`},{name:`duration`,global:!1,description:``,tags:[],required:!1,type:`number`,declarations:[],schema:`number`,default:`3200`},{name:`swipeDirection`,global:!1,description:``,tags:[],required:!1,type:`"right" | "left" | "up" | "down"`,declarations:[],schema:{kind:`enum`,type:`"right" | "left" | "up" | "down"`,schema:[`"right"`,`"left"`,`"up"`,`"down"`]},default:`"right"`},{name:`disableSwipe`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[{name:`label`,type:`string`,description:``,declarations:[],schema:`string`},{name:`duration`,type:`number`,description:``,declarations:[],schema:`number`},{name:`swipeDirection`,type:`"right" | "left" | "up" | "down"`,description:``,declarations:[],schema:{kind:`enum`,type:`"right" | "left" | "up" | "down"`,schema:[`"right"`,`"left"`,`"up"`,`"down"`]}},{name:`disableSwipe`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspToast/CspToastProvider.vue`})})),J,Y,X,Z,Q;e((()=>{r(),j(),H(),q(),J={title:`Éléments/Génériques/CspToast`,component:V,tags:[`autodocs`],parameters:{controls:{include:[`open`,`defaultOpen`,`title`,`description`,`duration`,`variant`,`showIcon`,`actionLabel`,`actionAltText`,`showClose`,`closeLabel`]},docs:{description:{component:`Notification toast accessible basée sur reka-ui. Doit être utilisé à l'intérieur d'un unique CspToastProvider placé à la racine de l'app.`}}},argTypes:{open:{control:{type:`boolean`},description:"État d'ouverture contrôlé. Liez avec `v-model:open`.",table:{type:{summary:`boolean`}}},defaultOpen:{control:{type:`boolean`},description:`État d'ouverture initial en mode non contrôlé.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},title:{control:{type:`text`},description:"Titre du toast (ou slot `title`).",table:{type:{summary:`string | null`}}},description:{control:{type:`text`},description:"Description du toast (ou slot `description`).",table:{type:{summary:`string | null`}}},duration:{control:{type:`number`},description:`Durée d'affichage en millisecondes. Hérite du provider si non défini.`,table:{type:{summary:`number`}}},variant:{control:{type:`radio`},options:[`default`,`info`,`success`,`warning`,`error`],description:`Variante visuelle de la notification.`,table:{type:{summary:`default | info | success | warning | error`},defaultValue:{summary:`default`}}},showIcon:{control:{type:`boolean`},description:`Affiche ou masque l'icone.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},actionLabel:{control:{type:`text`},description:`Label du bouton d'action.`,table:{type:{summary:`string | null`}}},actionAltText:{control:{type:`text`},description:`Texte alternatif annoncé pour l'action.`,table:{type:{summary:`string`},defaultValue:{summary:`Exécuter l'action`}}},showClose:{control:{type:`boolean`},description:`Affiche ou masque le bouton de fermeture.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},closeLabel:{control:{type:`text`},description:`Libellé accessible du bouton de fermeture.`,table:{type:{summary:`string`},defaultValue:{summary:`Fermer la notification`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{defaultOpen:!1,title:`Action terminée`,description:`Votre modification a bien été enregistrée.`,variant:`success`,showIcon:!0,actionLabel:`Annuler`,actionAltText:`Annuler la dernière action`,showClose:!0,closeLabel:`Fermer la notification`},render:e=>({components:{CspButton:M,CspToast:V,CspToastProvider:K},setup(){let n=t(!!e.open);m(()=>e.open,e=>{e!==void 0&&(n.value=e)});function r(){n.value=!0}function i(e){n.value=e}return{args:e,open:n,showToast:r,handleUpdateOpen:i}},template:`
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
    `})},Y={},X={render:e=>({components:{CspButton:M,CspToast:V,CspToastProvider:K},setup(){let n=[`default`,`info`,`success`,`warning`,`error`],r=t(!1),i=t(`default`);function a(e){i.value=e,r.value=!0}function o(e){r.value=e}return{args:e,variants:n,open:r,currentVariant:i,openVariant:a,updateOpen:o}},template:`
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
    `})},Z={render:()=>({components:{CspButton:M,CspToast:V,CspToastProvider:K},setup(){let e=t([]),n=0;function r(t){e.value.push({id:n++,variant:t,title:`Notification ${t} #${n}`})}function i(t){e.value=e.value.filter(e=>e.id!==t)}return{toasts:e,addToast:r,removeToast:i}},template:`
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