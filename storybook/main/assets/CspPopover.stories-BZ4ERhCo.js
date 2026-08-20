import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{D as t,E as n,F as r,K as i,P as a,R as o,S as s,Tt as c,V as l,W as u,X as d,Z as ee,c as f,k as te,m as p,mt as m,nt as h,vt as ne,x as g,xt as _}from"./iframe-Dhtaf6kn.js";import{E as re,T as ie,d as ae,g as oe,i as se,n as v,t as y,y as ce}from"./useForwardExpose-BG28srdR.js";import{n as le,t as b}from"./Primitive-wsFQogYy.js";import{n as x,t as S}from"./useId-yPTiDq1r.js";import{a as ue,i as de,n as fe,o as pe,r as C,t as me}from"./FocusScope-TCsSg-fK.js";import{n as he,t as ge}from"./useFocusGuards-CnjxJRtL.js";import{a as _e,c as ve,d as ye,f as be,l as w,n as xe,o as Se,r as Ce,s as we,u as T}from"./PopperContent-tzHiOpwV.js";import{n as Te,t as Ee}from"./Presence-DGpedCv5.js";import{a as De,n as E,r as Oe,t as ke}from"./Teleport-SLjkSbAE.js";import{n as Ae,t as D}from"./CspButton-DkgUEDOQ.js";import{n as je,t as Me}from"./useStoryOpenState-IvVsT5zZ.js";var O,k,A;function j(){return(j=e((()=>{re(),ve(),f(),se(),[O,k]=ie(`PopoverRoot`),A=t({__name:`PopoverRoot`,props:{defaultOpen:{type:Boolean,required:!1,default:!1},open:{type:Boolean,required:!1,default:void 0},modal:{type:Boolean,required:!1,default:!1}},emits:[`update:open`],setup(e,{emit:t}){let n=e,r=t,{modal:i}=ne(n),a=ae(n,`open`,r,{defaultValue:n.defaultOpen,passive:n.open===void 0}),o=m(),s=m(!1);return k({contentId:``,triggerId:``,modal:i,open:a,onOpenChange:e=>{a.value=e},onOpenToggle:()=>{a.value=!a.value},triggerElement:o,hasCustomAnchor:s}),(e,t)=>(l(),g(_(we),null,{default:h(()=>[u(e.$slots,`default`,{open:_(a),close:()=>a.value=!1})]),_:3}))}})})))()}var M;function N(){return(N=e((()=>{ge(),y(),ye(),De(),fe(),Ce(),j(),f(),oe(),M=t({__name:`PopoverContentImpl`,props:{trapFocus:{type:Boolean,required:!1},side:{type:null,required:!1},sideOffset:{type:Number,required:!1},sideFlip:{type:Boolean,required:!1},align:{type:null,required:!1},alignOffset:{type:Number,required:!1},alignFlip:{type:Boolean,required:!1},avoidCollisions:{type:Boolean,required:!1},collisionBoundary:{type:null,required:!1},collisionPadding:{type:[Number,Object],required:!1},arrowPadding:{type:Number,required:!1},hideShiftedArrow:{type:Boolean,required:!1},sticky:{type:String,required:!1},hideWhenDetached:{type:Boolean,required:!1},positionStrategy:{type:String,required:!1},updatePositionStrategy:{type:String,required:!1},disableUpdateOnLayoutShift:{type:Boolean,required:!1},prioritizePosition:{type:Boolean,required:!1},reference:{type:null,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1},disableOutsidePointerEvents:{type:Boolean,required:!1}},emits:[`escapeKeyDown`,`pointerDownOutside`,`focusOutside`,`interactOutside`,`openAutoFocus`,`closeAutoFocus`],setup(e,{emit:t}){let i=e,a=t,o=be(ce(i,`trapFocus`,`disableOutsidePointerEvents`)),{forwardRef:s}=v(),c=O();return he(),(e,t)=>(l(),g(_(me),{"as-child":``,loop:``,trapped:e.trapFocus,onMountAutoFocus:t[5]||=e=>a(`openAutoFocus`,e),onUnmountAutoFocus:t[6]||=e=>a(`closeAutoFocus`,e)},{default:h(()=>[n(_(Oe),{"as-child":``,"disable-outside-pointer-events":e.disableOutsidePointerEvents,onPointerDownOutside:t[0]||=e=>a(`pointerDownOutside`,e),onInteractOutside:t[1]||=e=>a(`interactOutside`,e),onEscapeKeyDown:t[2]||=e=>a(`escapeKeyDown`,e),onFocusOutside:t[3]||=e=>a(`focusOutside`,e),onDismiss:t[4]||=e=>_(c).onOpenChange(!1)},{default:h(()=>[n(_(xe),r(_(o),{id:_(c).contentId,ref:_(s),"data-state":_(c).open.value?`open`:`closed`,"aria-labelledby":_(c).triggerId,style:{"--reka-popover-content-transform-origin":`var(--reka-popper-transform-origin)`,"--reka-popover-content-available-width":`var(--reka-popper-available-width)`,"--reka-popover-content-available-height":`var(--reka-popper-available-height)`,"--reka-popover-trigger-width":`var(--reka-popper-anchor-width)`,"--reka-popover-trigger-height":`var(--reka-popper-anchor-height)`},role:`dialog`}),{default:h(()=>[u(e.$slots,`default`)]),_:3},16,[`id`,`data-state`,`aria-labelledby`])]),_:3},8,[`disable-outside-pointer-events`])]),_:3},8,[`trapped`]))}})})))()}var P;function F(){return(F=e((()=>{ue(),y(),w(),C(),j(),N(),f(),P=t({__name:`PopoverContentModal`,props:{side:{type:null,required:!1},sideOffset:{type:Number,required:!1},sideFlip:{type:Boolean,required:!1},align:{type:null,required:!1},alignOffset:{type:Number,required:!1},alignFlip:{type:Boolean,required:!1},avoidCollisions:{type:Boolean,required:!1},collisionBoundary:{type:null,required:!1},collisionPadding:{type:[Number,Object],required:!1},arrowPadding:{type:Number,required:!1},hideShiftedArrow:{type:Boolean,required:!1},sticky:{type:String,required:!1},hideWhenDetached:{type:Boolean,required:!1},positionStrategy:{type:String,required:!1},updatePositionStrategy:{type:String,required:!1},disableUpdateOnLayoutShift:{type:Boolean,required:!1},prioritizePosition:{type:Boolean,required:!1},reference:{type:null,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1},disableOutsidePointerEvents:{type:Boolean,required:!1}},emits:[`escapeKeyDown`,`pointerDownOutside`,`focusOutside`,`interactOutside`,`openAutoFocus`,`closeAutoFocus`],setup(e,{emit:t}){let n=e,i=t,a=O(),o=m(!1);pe(!0);let s=T(n,i),{forwardRef:c,currentElement:d}=v();return de(d),(e,t)=>(l(),g(M,r(_(s),{ref:_(c),"trap-focus":_(a).open.value,"disable-outside-pointer-events":``,onCloseAutoFocus:t[0]||=p(e=>{i(`closeAutoFocus`,e),o.value||_(a).triggerElement.value?.focus()},[`prevent`]),onPointerDownOutside:t[1]||=e=>{i(`pointerDownOutside`,e);let t=e.detail.originalEvent,n=t.button===0&&t.ctrlKey===!0,r=t.button===2||n;o.value=r},onFocusOutside:t[2]||=p(()=>{},[`prevent`])}),{default:h(()=>[u(e.$slots,`default`)]),_:3},16,[`trap-focus`]))}})})))()}var I;function L(){return(L=e((()=>{w(),j(),N(),f(),I=t({__name:`PopoverContentNonModal`,props:{side:{type:null,required:!1},sideOffset:{type:Number,required:!1},sideFlip:{type:Boolean,required:!1},align:{type:null,required:!1},alignOffset:{type:Number,required:!1},alignFlip:{type:Boolean,required:!1},avoidCollisions:{type:Boolean,required:!1},collisionBoundary:{type:null,required:!1},collisionPadding:{type:[Number,Object],required:!1},arrowPadding:{type:Number,required:!1},hideShiftedArrow:{type:Boolean,required:!1},sticky:{type:String,required:!1},hideWhenDetached:{type:Boolean,required:!1},positionStrategy:{type:String,required:!1},updatePositionStrategy:{type:String,required:!1},disableUpdateOnLayoutShift:{type:Boolean,required:!1},prioritizePosition:{type:Boolean,required:!1},reference:{type:null,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1},disableOutsidePointerEvents:{type:Boolean,required:!1}},emits:[`escapeKeyDown`,`pointerDownOutside`,`focusOutside`,`interactOutside`,`openAutoFocus`,`closeAutoFocus`],setup(e,{emit:t}){let n=e,i=t,a=O(),o=m(!1),s=m(!1),c=T(n,i);return(e,t)=>(l(),g(M,r(_(c),{"trap-focus":!1,"disable-outside-pointer-events":!1,onCloseAutoFocus:t[0]||=e=>{i(`closeAutoFocus`,e),e.defaultPrevented||(o.value||_(a).triggerElement.value?.focus(),e.preventDefault()),o.value=!1,s.value=!1},onInteractOutside:t[1]||=async e=>{i(`interactOutside`,e),e.defaultPrevented||(o.value=!0,e.detail.originalEvent.type===`pointerdown`&&(s.value=!0));let t=e.target;_(a).triggerElement.value?.contains(t)&&e.preventDefault(),e.detail.originalEvent.type===`focusin`&&s.value&&e.preventDefault()}}),{default:h(()=>[u(e.$slots,`default`)]),_:3},16))}})})))()}var R;function z(){return(z=e((()=>{y(),w(),S(),Te(),j(),F(),L(),f(),R=t({__name:`PopoverContent`,props:{forceMount:{type:Boolean,required:!1},side:{type:null,required:!1},sideOffset:{type:Number,required:!1},sideFlip:{type:Boolean,required:!1},align:{type:null,required:!1},alignOffset:{type:Number,required:!1},alignFlip:{type:Boolean,required:!1},avoidCollisions:{type:Boolean,required:!1},collisionBoundary:{type:null,required:!1},collisionPadding:{type:[Number,Object],required:!1},arrowPadding:{type:Number,required:!1},hideShiftedArrow:{type:Boolean,required:!1},sticky:{type:String,required:!1},hideWhenDetached:{type:Boolean,required:!1},positionStrategy:{type:String,required:!1},updatePositionStrategy:{type:String,required:!1},disableUpdateOnLayoutShift:{type:Boolean,required:!1},prioritizePosition:{type:Boolean,required:!1},reference:{type:null,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1},disableOutsidePointerEvents:{type:Boolean,required:!1}},emits:[`escapeKeyDown`,`pointerDownOutside`,`focusOutside`,`interactOutside`,`openAutoFocus`,`closeAutoFocus`],setup(e,{emit:t}){let n=e,i=t,a=O(),o=T(n,i),{forwardRef:s}=v();return a.contentId||=x(void 0,`reka-popover-content`),(e,t)=>(l(),g(_(Ee),{present:e.forceMount||_(a).open.value},{default:h(()=>[_(a).modal.value?(l(),g(P,r({key:0},_(o),{ref:_(s)}),{default:h(()=>[u(e.$slots,`default`)]),_:3},16)):(l(),g(I,r({key:1},_(o),{ref:_(s)}),{default:h(()=>[u(e.$slots,`default`)]),_:3},16))]),_:3},8,[`present`]))}})})))()}var B;function V(){return(V=e((()=>{E(),f(),B=t({__name:`PopoverPortal`,props:{to:{type:null,required:!1},disabled:{type:Boolean,required:!1},defer:{type:Boolean,required:!1},forceMount:{type:Boolean,required:!1}},setup(e){let t=e;return(e,n)=>(l(),g(_(ke),c(te(t)),{default:h(()=>[u(e.$slots,`default`)]),_:3},16))}})})))()}var H;function U(){return(U=e((()=>{y(),S(),le(),Se(),j(),f(),H=t({__name:`PopoverTrigger`,props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:`button`}},setup(e){let t=e,r=O(),{forwardRef:a,currentElement:s}=v();return r.triggerId||=x(void 0,`reka-popover-trigger`),o(()=>{r.triggerElement.value=s.value}),(e,o)=>(l(),g(i(_(r).hasCustomAnchor.value?_(b):_(_e)),{"as-child":``},{default:h(()=>[n(_(b),{id:_(r).triggerId,ref:_(a),type:e.as===`button`?`button`:void 0,"aria-haspopup":`dialog`,"aria-expanded":_(r).open.value,"aria-controls":_(r).contentId,"data-state":_(r).open.value?`open`:`closed`,as:e.as,"as-child":t.asChild,onClick:_(r).onOpenToggle},{default:h(()=>[u(e.$slots,`default`)]),_:3},8,[`id`,`type`,`aria-expanded`,`aria-controls`,`data-state`,`as`,`as-child`,`onClick`])]),_:3}))}})})))()}var W;function G(){return(G=e((()=>{f(),z(),V(),j(),U(),W=t({inheritAttrs:!1,__name:`CspPopover`,props:a({side:{default:`bottom`},align:{default:`start`}},{open:{type:Boolean},openModifiers:{}}),emits:[`update:open`],setup(e){let t=d(e,`open`),r=!!ee().trigger;return(i,a)=>(l(),g(_(A),{open:t.value,"onUpdate:open":a[0]||=e=>t.value=e},{default:h(()=>[_(r)?(l(),g(_(H),{key:0,"as-child":``},{default:h(()=>[u(i.$slots,`trigger`)]),_:3})):s(``,!0),n(_(B),null,{default:h(()=>[n(_(R),{class:`csp-popover`,side:e.side,align:e.align,"side-offset":6},{default:h(()=>[u(i.$slots,`default`)]),_:3},8,[`side`,`align`])]),_:3})]),_:3},8,[`open`]))}})})))()}var K;function q(){return(q=e((()=>{G(),K=W})))()}var J,Y,X,Z,Q;function $(){return($=e((()=>{Ae(),q(),Me(),J={title:`Éléments/Génériques/CspPopover`,component:K,tags:[`autodocs`],parameters:{controls:{include:[`open`,`side`,`align`]},docs:{description:{component:"Popover générique construit sur la primitive `reka-ui`. Affiche un contenu flottant ancré à un déclencheur via le slot `trigger`. Gère le focus, la touche Échap et le clic extérieur. Le slot par défaut reçoit le contenu libre."}},layout:`centered`},argTypes:{open:{control:{type:`boolean`},description:"État d'ouverture contrôlé. Liez avec `v-model:open`.",table:{type:{summary:`boolean`}}},side:{control:{type:`radio`},options:[`top`,`right`,`bottom`,`left`],description:`Côté d'apparition du popover.`,table:{type:{summary:`top | right | bottom | left`},defaultValue:{summary:`bottom`}}},align:{control:{type:`radio`},options:[`start`,`center`,`end`],description:`Alignement du popover par rapport au déclencheur.`,table:{type:{summary:`start | center | end`},defaultValue:{summary:`start`}}},trigger:{control:!1,table:{disable:!0}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{side:`bottom`,align:`start`},render:e=>({components:{CspPopover:K,CspButton:D},setup(){let{controlledOpen:t,handleUpdateOpen:n,open:r}=je(e);return{args:e,controlledOpen:t,handleUpdateOpen:n,open:r}},template:`
      <CspPopover v-bind="args" :open="controlledOpen" @update:open="handleUpdateOpen">
        <template #trigger>
          <CspButton
            :label="(open ? 'Fermer' : 'Ouvrir') + ' le popover'"
            variant="secondary"
            icon="ri:settings-3-line"
            :is-icon-left="true"
          />
        </template>

        <p class="text-sm">Contenu libre du popover.</p>
      </CspPopover>
    `})},Y={name:`Par défaut`},X={name:`Côtés`,render:e=>({components:{CspPopover:K,CspButton:D},setup(){return{args:e,sides:[{label:`Haut`,value:`top`},{label:`Droite`,value:`right`},{label:`Bas`,value:`bottom`},{label:`Gauche`,value:`left`}]}},template:`
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 justify-items-center">
        <div v-for="s in sides" :key="s.value" class="p-8">
          <CspPopover
            v-bind="args"
            :side="s.value"
          >
            <template #trigger>
              <CspButton
                :label="(controlledOpen ? 'Fermer' : 'Ouvrir') + ' le popover côté ' + s.label.toLowerCase()"
                variant="secondary"
                icon="ri:settings-3-line"
                :is-icon-left="true"
              />
            </template>

            <p class="text-sm">Contenu libre du popover</p>
          </CspPopover>
        </div>
      </div>
    `})},Z={name:`Alignements`,render:e=>({components:{CspPopover:K,CspButton:D},setup(){return{args:e,alignments:[{label:`Début`,value:`start`},{label:`Centre`,value:`center`},{label:`Fin`,value:`end`}]}},template:`
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 justify-items-center">
        <div v-for="a in alignments" :key="a.value" class="p-8">
          <CspPopover
            v-bind="args"
            :align="a.value"
          >
            <template #trigger>
              <CspButton
                :label="(controlledOpen ? 'Fermer' : 'Ouvrir') + ' le popover aligné ' + a.label.toLowerCase()"
                variant="secondary"
                icon="ri:settings-3-line"
                :is-icon-left="true"
              />
            </template>
            <p class="text-sm">Contenu libre du popover</p>
          </CspPopover>
        </div>
      </div>
    `})},Y.parameters={...Y.parameters,docs:{...Y.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...Y.parameters?.docs?.source}}},X.parameters={...X.parameters,docs:{...X.parameters?.docs,source:{originalSource:`{
  name: 'Côtés',
  render: (args: CspPopoverProps) => ({
    components: {
      CspPopover,
      CspButton
    },
    setup() {
      const sides = [{
        label: 'Haut',
        value: 'top'
      }, {
        label: 'Droite',
        value: 'right'
      }, {
        label: 'Bas',
        value: 'bottom'
      }, {
        label: 'Gauche',
        value: 'left'
      }] satisfies {
        label: string;
        value: NonNullable<CspPopoverProps['side']>;
      }[];
      return {
        args,
        sides
      };
    },
    template: \`
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 justify-items-center">
        <div v-for="s in sides" :key="s.value" class="p-8">
          <CspPopover
            v-bind="args"
            :side="s.value"
          >
            <template #trigger>
              <CspButton
                :label="(controlledOpen ? 'Fermer' : 'Ouvrir') + ' le popover côté ' + s.label.toLowerCase()"
                variant="secondary"
                icon="ri:settings-3-line"
                :is-icon-left="true"
              />
            </template>

            <p class="text-sm">Contenu libre du popover</p>
          </CspPopover>
        </div>
      </div>
    \`
  })
}`,...X.parameters?.docs?.source}}},Z.parameters={...Z.parameters,docs:{...Z.parameters?.docs,source:{originalSource:`{
  name: 'Alignements',
  render: (args: CspPopoverProps) => ({
    components: {
      CspPopover,
      CspButton
    },
    setup() {
      const alignments = [{
        label: 'Début',
        value: 'start'
      }, {
        label: 'Centre',
        value: 'center'
      }, {
        label: 'Fin',
        value: 'end'
      }] satisfies {
        label: string;
        value: NonNullable<CspPopoverProps['align']>;
      }[];
      return {
        args,
        alignments
      };
    },
    template: \`
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 justify-items-center">
        <div v-for="a in alignments" :key="a.value" class="p-8">
          <CspPopover
            v-bind="args"
            :align="a.value"
          >
            <template #trigger>
              <CspButton
                :label="(controlledOpen ? 'Fermer' : 'Ouvrir') + ' le popover aligné ' + a.label.toLowerCase()"
                variant="secondary"
                icon="ri:settings-3-line"
                :is-icon-left="true"
              />
            </template>
            <p class="text-sm">Contenu libre du popover</p>
          </CspPopover>
        </div>
      </div>
    \`
  })
}`,...Z.parameters?.docs?.source}}},Q=[`Default`,`Sides`,`Alignments`]})))()}$();export{Z as Alignments,Y as Default,X as Sides,Q as __namedExportsOrder,J as default};