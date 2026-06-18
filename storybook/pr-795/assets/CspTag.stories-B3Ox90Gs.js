import{i as e}from"./preload-helper-CnUkjUDP.js";import{C as t,I as n,J as r,K as i,L as a,Mt as o,P as s,Rt as c,Tt as l,V as u,Y as d,at as ee,it as f,lt as p,mt as m,nt as h,tt as g,z as _}from"./iframe-BYp246MG.js";import{n as v,t as y}from"./_plugin-vue_export-helper-BbC-fNz1.js";import{Jt as b,g as x,m as S,t as C,v as w}from"./dist-BPvPpfGQ.js";import{n as T,t as E}from"./CspIcon-Cwg9sIgV.js";function D(e){switch(e.variant){case`selectable`:return e.inGroup?`toggle-group-item`:`toggle`;case`clickable`:return e.hasHref&&!e.disabled?`a`:`button`;case`dismissible`:return`button`;case`static`:return`p`;default:return`p`}}function O(e,t){return e||(t?`Retirer le filtre ${t}`:void 0)}var k=e((()=>{D.__docgenInfo=Object.assign({displayName:D.name??D.__name},{exportName:`resolveTagRoot`,displayName:`resolveTagRoot`,type:2,props:[{name:`variant`,global:!1,description:``,tags:[],required:!0,type:`CspTagVariant`,declarations:[],schema:{kind:`enum`,type:`CspTagVariant`,schema:[`"static"`,`"clickable"`,`"selectable"`,`"dismissible"`]}},{name:`inGroup`,global:!1,description:``,tags:[],required:!0,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`disabled`,global:!1,description:``,tags:[],required:!0,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`hasHref`,global:!1,description:``,tags:[],required:!0,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspTag/tag.ts`}),O.__docgenInfo=Object.assign({displayName:O.name??O.__name},{exportName:`resolveDismissAriaLabel`,displayName:`resolveDismissAriaLabel`,type:2,props:[{name:`toString`,global:!1,description:`Returns a string representation of a string.`,tags:[],required:!0,type:`() => string`,declarations:[],schema:{kind:`event`,type:`(): string`}},{name:`charAt`,global:!1,description:`Returns the character at the specified index.`,tags:[{name:`param`,text:`pos The zero-based index of the desired character.`}],required:!0,type:`(pos: number) => string`,declarations:[],schema:{kind:`event`,type:`(pos: number): string`}},{name:`charCodeAt`,global:!1,description:`Returns the Unicode value of the character at the specified location.`,tags:[{name:`param`,text:`index The zero-based index of the desired character. If there is no character at the specified index, NaN is returned.`}],required:!0,type:`(index: number) => number`,declarations:[],schema:{kind:`event`,type:`(index: number): number`}},{name:`concat`,global:!1,description:`Returns a string that contains the concatenation of two or more strings.`,tags:[{name:`param`,text:`strings The strings to append to the end of the string.`}],required:!0,type:`(...strings: string[]) => string`,declarations:[],schema:{kind:`event`,type:`(...strings: string[]): string`}},{name:`indexOf`,global:!1,description:`Returns the position of the first occurrence of a substring.`,tags:[{name:`param`,text:`searchString The substring to search for in the string`},{name:`param`,text:`position The index at which to begin searching the String object. If omitted, search starts at the beginning of the string.`}],required:!0,type:`(searchString: string, position?: number) => number`,declarations:[],schema:{kind:`event`,type:`(searchString: string, position?: number): number`}},{name:`lastIndexOf`,global:!1,description:`Returns the last occurrence of a substring in the string.`,tags:[{name:`param`,text:`searchString The substring to search for.`},{name:`param`,text:`position The index at which to begin searching. If omitted, the search begins at the end of the string.`}],required:!0,type:`(searchString: string, position?: number) => number`,declarations:[],schema:{kind:`event`,type:`(searchString: string, position?: number): number`}},{name:`localeCompare`,global:!1,description:`Determines whether two strings are equivalent in the current locale.
Determines whether two strings are equivalent in the current or specified locale.`,tags:[{name:`param`,text:`that String to compare to target string`},{name:`param`,text:`that String to compare to target string`},{name:`param`,text:`locales A locale string or array of locale strings that contain one or more language or locale tags. If you include more than one locale string, list them in descending order of priority so that the first entry is the preferred locale. If you omit this parameter, the default locale of the JavaScript runtime is used. This parameter must conform to BCP 47 standards; see the Intl.Collator object for details.`},{name:`param`,text:`options An object that contains one or more properties that specify comparison options. see the Intl.Collator object for details.`}],required:!0,type:`{ (that: string): number; (that: string, locales?: string | string[], options?: CollatorOptions): number; }`,declarations:[],schema:`{ (that: string): number; (that: string, locales?: string | string[], options?: CollatorOptions): number; }`},{name:`match`,global:!1,description:`Matches a string with a regular expression, and returns an array containing the results of that search.`,tags:[{name:`param`,text:`regexp A variable name or string literal containing the regular expression pattern and flags.`}],required:!0,type:`(regexp: string | RegExp) => RegExpMatchArray`,declarations:[],schema:{kind:`event`,type:`(regexp: string | RegExp): RegExpMatchArray`}},{name:`replace`,global:!1,description:`Replaces text in a string, using a regular expression or search string.`,tags:[{name:`param`,text:`searchValue A string or regular expression to search for.`},{name:`param`,text:"replaceValue A string containing the text to replace. When the {@linkcode searchValue} is a `RegExp`, all matches are replaced if the `g` flag is set (or only those matches at the beginning, if the `y` flag is also present). Otherwise, only the first match of {@linkcode searchValue} is replaced."},{name:`param`,text:`searchValue A string to search for.`},{name:`param`,text:`replacer A function that returns the replacement text.`}],required:!0,type:`{ (searchValue: string | RegExp, replaceValue: string): string; (searchValue: string | RegExp, replacer: (substring: string, ...args: any[]) => string): string; }`,declarations:[],schema:`{ (searchValue: string | RegExp, replaceValue: string): string; (searchValue: string | RegExp, replacer: (substring: string, ...args: any[]) => string): string; }`},{name:`search`,global:!1,description:`Finds the first substring match in a regular expression search.`,tags:[{name:`param`,text:`regexp The regular expression pattern and applicable flags.`}],required:!0,type:`(regexp: string | RegExp) => number`,declarations:[],schema:{kind:`event`,type:`(regexp: string | RegExp): number`}},{name:`slice`,global:!1,description:`Returns a section of a string.`,tags:[{name:`param`,text:`start The index to the beginning of the specified portion of stringObj.`},{name:`param`,text:`end The index to the end of the specified portion of stringObj. The substring includes the characters up to, but not including, the character indicated by end.
If this value is not specified, the substring continues to the end of stringObj.`}],required:!0,type:`(start?: number, end?: number) => string`,declarations:[],schema:{kind:`event`,type:`(start?: number, end?: number): string`}},{name:`split`,global:!1,description:`Split a string into substrings using the specified separator and return them as an array.`,tags:[{name:`param`,text:`separator A string that identifies character or characters to use in separating the string. If omitted, a single-element array containing the entire string is returned.`},{name:`param`,text:`limit A value used to limit the number of elements returned in the array.`}],required:!0,type:`(separator: string | RegExp, limit?: number) => string[]`,declarations:[],schema:{kind:`event`,type:`(separator: string | RegExp, limit?: number): string[]`}},{name:`substring`,global:!1,description:`Returns the substring at the specified location within a String object.`,tags:[{name:`param`,text:`start The zero-based index number indicating the beginning of the substring.`},{name:`param`,text:`end Zero-based index number indicating the end of the substring. The substring includes the characters up to, but not including, the character indicated by end.
If end is omitted, the characters from start through the end of the original string are returned.`}],required:!0,type:`(start: number, end?: number) => string`,declarations:[],schema:{kind:`event`,type:`(start: number, end?: number): string`}},{name:`toLowerCase`,global:!1,description:`Converts all the alphabetic characters in a string to lowercase.`,tags:[],required:!0,type:`() => string`,declarations:[],schema:{kind:`event`,type:`(): string`}},{name:`toLocaleLowerCase`,global:!1,description:`Converts all alphabetic characters to lowercase, taking into account the host environment's current locale.`,tags:[],required:!0,type:`(locales?: string | string[]) => string`,declarations:[],schema:{kind:`event`,type:`(locales?: string | string[]): string`}},{name:`toUpperCase`,global:!1,description:`Converts all the alphabetic characters in a string to uppercase.`,tags:[],required:!0,type:`() => string`,declarations:[],schema:{kind:`event`,type:`(): string`}},{name:`toLocaleUpperCase`,global:!1,description:`Returns a string where all alphabetic characters have been converted to uppercase, taking into account the host environment's current locale.`,tags:[],required:!0,type:`(locales?: string | string[]) => string`,declarations:[],schema:{kind:`event`,type:`(locales?: string | string[]): string`}},{name:`trim`,global:!1,description:`Removes the leading and trailing white space and line terminator characters from a string.`,tags:[],required:!0,type:`() => string`,declarations:[],schema:{kind:`event`,type:`(): string`}},{name:`length`,global:!1,description:`Returns the length of a String object.`,tags:[],required:!0,type:`number`,declarations:[],schema:`number`},{name:`substr`,global:!1,description:`Gets a substring beginning at the specified location and having the specified length.`,tags:[{name:`deprecated`,text:`A legacy feature for browser compatibility`},{name:`param`,text:`from The starting position of the desired substring. The index of the first character in the string is zero.`},{name:`param`,text:`length The number of characters to include in the returned substring.`}],required:!0,type:`(from: number, length?: number) => string`,declarations:[],schema:{kind:`event`,type:`(from: number, length?: number): string`}},{name:`valueOf`,global:!1,description:`Returns the primitive value of the specified object.`,tags:[],required:!0,type:`() => string`,declarations:[],schema:{kind:`event`,type:`(): string`}}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspTag/tag.ts`})}));function A(e){h(M,e)}function j(){return i(M,null)}var M,N=e((()=>{t(),M=Symbol(`CspTagGroup`),A.__docgenInfo=Object.assign({displayName:A.name??A.__name},{exportName:`provideCspTagGroup`,displayName:`provideCspTagGroup`,type:2,props:[{name:`size`,global:!1,description:``,tags:[],required:!1,type:`CspTagSize`,declarations:[],schema:{kind:`enum`,type:`CspTagSize`,schema:[`"md"`,`"sm"`,`"lg"`]}},{name:`disabled`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspTag/useCspTagGroup.ts`})})),P,F=e((()=>{t(),C(),T(),k(),N(),P=u({__name:`CspTag`,props:r({size:{},label:{},disabled:{type:Boolean},icon:{},as:{},asChild:{type:Boolean},variant:{},href:{},value:{},dismissLabel:{}},{pressed:{type:Boolean,default:!1},pressedModifiers:{}}),emits:r([`dismiss`],[`update:pressed`]),setup(e,{emit:t}){let r=e,i=t,o=s(()=>r.variant??`static`),l=p(e,`pressed`),u=j(),f=s(()=>r.size??u?.size??`md`),h=s(()=>r.disabled??u?.disabled??!1),v=s(()=>o.value!==`static`&&o.value!==`dismissible`),y=s(()=>o.value===`selectable`&&u!==null),C=s(()=>`icon`in r?r.icon:void 0),w=s(()=>`href`in r?r.href:void 0),T=s(()=>`as`in r?r.as:void 0),k=s(()=>`asChild`in r?r.asChild:void 0),A=s(()=>O(`dismissLabel`in r?r.dismissLabel:void 0,r.label)),M=s(()=>{switch(D({variant:o.value,inGroup:y.value,disabled:h.value,hasHref:!!w.value})){case`toggle-group-item`:return{is:S,attrs:{value:`value`in r?r.value:void 0,disabled:h.value}};case`toggle`:return{is:x,attrs:{modelValue:l.value,"onUpdate:modelValue":e=>{l.value=e},disabled:h.value}};case`a`:return{is:b,attrs:{as:T.value??`a`,asChild:k.value,href:w.value}};case`button`:return{is:b,attrs:o.value===`dismissible`?{as:`button`,type:`button`,disabled:h.value,"aria-label":A.value,onClick:()=>i(`dismiss`)}:{as:T.value??`button`,asChild:k.value,type:`button`,disabled:h.value}};default:return{is:b,attrs:{as:T.value??`p`,asChild:k.value}}}});return(t,r)=>(g(),n(ee(M.value.is),d(M.value.attrs,{class:[`csp-tag`,[`csp-tag--${f.value}`,{"csp-tag--interactive":v.value,"csp-tag--dismissible":o.value===`dismissible`}]]}),{default:m(()=>[C.value?(g(),n(E,{key:0,class:`csp-tag__icon`,name:C.value,"aria-hidden":`true`},null,8,[`name`])):a(``,!0),_(` `+c(e.label)+` `,1),o.value===`dismissible`?(g(),n(E,{key:1,class:`csp-tag__dismiss`,name:`ri:close-line`,"aria-hidden":`true`})):a(``,!0)]),_:1},16,[`class`]))}})})),I=e((()=>{})),L,R=e((()=>{F(),F(),I(),v(),L=y(P,[[`__scopeId`,`data-v-49d39347`]]),P.__docgenInfo=Object.assign({displayName:P.name??P.__name},{exportName:`default`,displayName:`CspTag`,type:1,props:[{name:`size`,global:!1,description:``,tags:[],required:!1,type:`CspTagSize`,declarations:[],schema:{kind:`enum`,type:`CspTagSize`,schema:[`"md"`,`"sm"`,`"lg"`]}},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`variant`,global:!1,description:``,tags:[],required:!1,type:`"static" | "clickable" | "selectable" | "dismissible"`,declarations:[],schema:{kind:`enum`,type:`"static" | "clickable" | "selectable" | "dismissible"`,schema:[`"static"`,`"clickable"`,`"selectable"`,`"dismissible"`]}},{name:`label`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`disabled`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`pressed`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`}],events:[{name:`update:pressed`,description:``,tags:[],type:`[value: boolean]`,signature:`(event: "update:pressed", value: boolean): void`,declarations:[],schema:[{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}]},{name:`dismiss`,description:``,tags:[],type:`[]`,signature:`(event: "dismiss"): void`,declarations:[],schema:[]}],slots:[],exposed:[{name:`size`,type:`CspTagSize`,description:``,declarations:[],schema:{kind:`enum`,type:`CspTagSize`,schema:[`"md"`,`"sm"`,`"lg"`]}},{name:`variant`,type:`"static" | "clickable" | "selectable" | "dismissible"`,description:``,declarations:[],schema:{kind:`enum`,type:`"static" | "clickable" | "selectable" | "dismissible"`,schema:[`"static"`,`"clickable"`,`"selectable"`,`"dismissible"`]}},{name:`label`,type:`string`,description:``,declarations:[],schema:`string`},{name:`disabled`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`pressed`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspTag/CspTag.vue`})})),z,B=e((()=>{t(),C(),N(),z=u({__name:`CspTagGroup`,props:r({type:{default:`multiple`},size:{},disabled:{type:Boolean,default:!1},loop:{type:Boolean,default:!0}},{modelValue:{},modelModifiers:{}}),emits:[`update:modelValue`],setup(e){let t=e,r=p(e,`modelValue`);return A({size:t.size,disabled:t.disabled}),(t,i)=>(g(),n(o(w),{modelValue:r.value,"onUpdate:modelValue":i[0]||=e=>r.value=e,class:`csp-tag-group`,type:e.type,disabled:e.disabled,loop:e.loop,"roving-focus":!0},{default:m(()=>[f(t.$slots,`default`,{},void 0,!0)]),_:3},8,[`modelValue`,`type`,`disabled`,`loop`]))}})})),V=e((()=>{})),H,te=e((()=>{B(),B(),V(),v(),H=y(z,[[`__scopeId`,`data-v-53ec5618`]]),z.__docgenInfo=Object.assign({displayName:z.name??z.__name},{exportName:`default`,displayName:`CspTagGroup`,type:2,props:[{name:`type`,global:!1,description:``,tags:[],required:!1,type:`"single" | "multiple"`,declarations:[],schema:{kind:`enum`,type:`"single" | "multiple"`,schema:[`"single"`,`"multiple"`]},default:`"multiple"`},{name:`size`,global:!1,description:``,tags:[],required:!1,type:`CspTagSize`,declarations:[],schema:{kind:`enum`,type:`CspTagSize`,schema:[`"md"`,`"sm"`,`"lg"`]}},{name:`disabled`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`loop`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`true`},{name:`modelValue`,global:!1,description:``,tags:[],required:!1,type:`string | number | (string | number)[]`,declarations:[],schema:{kind:`enum`,type:`string | number | (string | number)[]`,schema:[`string`,`number`,{kind:`array`,type:`(string | number)[]`}]}},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[{name:`update:modelValue`,description:``,tags:[],type:`[value: string | number | (string | number)[]]`,signature:`(evt: "update:modelValue", value: string | number | (string | number)[]): void`,declarations:[],schema:[{kind:`enum`,type:`string | number | (string | number)[]`,schema:[`string`,`number`,{kind:`array`,type:`(string | number)[]`}]}]}],slots:[{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspTag/CspTagGroup.vue`})})),U,W,G,K,q,J,Y,X,Z,Q,$;e((()=>{t(),R(),te(),U={title:`Éléments/Génériques/CspTag`,component:L,tags:[`autodocs`],parameters:{controls:{include:[`label`,`variant`,`size`,`icon`,`pressed`,`disabled`,`href`,`value`,`dismissLabel`]},docs:{description:{component:"Étiquette générique. Sert à **catégoriser ou filtrer** les contenus (à ne pas confondre avec `CspBadge` qui signale un état).\n\nConstruit sur les primitives [reka-ui](https://reka-ui.com) :\n- `static` et `clickable` reposent sur le composant `Primitive` de reka et sont polymorphes via `as` / `asChild` ;\n- `dismissible` est toujours un `<button>` ;\n- `selectable` repose sur le composant reka `Toggle` rendu seul, ou sur `ToggleGroupItem` lorsqu'il est placé dans un `CspTagGroup`.\n"}}},argTypes:{label:{control:{type:`text`},description:`Libellé du tag (cas simple). Pour un contenu riche, utiliser le slot par défaut.`,table:{type:{summary:`string`}}},variant:{control:{type:`radio`},options:[`static`,`clickable`,`selectable`,`dismissible`],description:`Mode d'interaction du tag.`,table:{type:{summary:`static | clickable | selectable | dismissible`},defaultValue:{summary:`static`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:"Taille du tag. Héritée du `CspTagGroup` si non précisée.",table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},icon:{control:{type:`text`},description:"Icône Iconify affichée à gauche. Non disponible sur `dismissible` (croix exclusive).",table:{type:{summary:`string`}}},pressed:{control:{type:`boolean`},description:"État activé du tag `selectable` autonome. Lier avec `v-model:pressed`.",table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},disabled:{control:{type:`boolean`},description:"Désactive les variantes interactives. Héritée du `CspTagGroup`.",table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},href:{control:{type:`text`},description:"URL cible pour la variante `clickable`. Rend un `<a>` si fourni, sinon un `<button>`.",table:{type:{summary:`string`}}},value:{control:{type:`text`},description:"Identifiant d'un tag `selectable` au sein d'un `CspTagGroup`.",table:{type:{summary:`string | number`}}},dismissLabel:{control:{type:`text`},description:"Label accessible du bouton de suppression (`dismissible`). Par défaut : `Retirer le filtre {label}`.",table:{type:{summary:`string`}}},as:{control:!1,table:{disable:!0}},asChild:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{label:`Libellé`,variant:`static`,size:`md`,pressed:!1,disabled:!1},render:e=>({components:{CspTag:L},setup(){return{args:e,pressed:l(!!e.pressed)}},template:`
      <CspTag
        v-bind="args"
        v-model:pressed="pressed"
        @dismiss="() => {}"
      />
    `})},W=[`sm`,`md`,`lg`],G={name:`Par défaut`},K={name:`Variantes`,render:()=>({components:{CspTag:L},setup(){return{pressed:l(!1),dismissed:l(!1)}},template:`
      <div class="flex flex-col gap-6">
        <div>
          <p class="mb-2 text-sm text-text-mention-grey">static (étiquette)</p>
          <CspTag label="Catégorie" variant="static" />
        </div>
        <div>
          <p class="mb-2 text-sm text-text-mention-grey">clickable (lien)</p>
          <CspTag label="Voir tout" variant="clickable" href="#" />
        </div>
        <div>
          <p class="mb-2 text-sm text-text-mention-grey">selectable (filtre à bascule / {{ pressed ? 'actif' : 'inactif' }})</p>
          <CspTag label="Filtre A" variant="selectable" v-model:pressed="pressed" />
        </div>
        <div>
          <p class="mb-2 text-sm text-text-mention-grey">dismissible : filtre actif à retirer</p>
          <CspTag v-if="!dismissed" label="Filtre actif" variant="dismissible" @dismiss="dismissed = true" />
          <span v-else class="text-sm text-text-mention-grey italic">retiré</span>
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},q={name:`Avec icône`,render:()=>({components:{CspTag:L},template:`
      <div class="flex flex-row gap-4 flex-wrap">
        <CspTag label="Étiquette" variant="static" icon="ri:bookmark-line" />
        <CspTag label="Lien" variant="clickable" icon="ri:external-link-line" href="#" />
        <CspTag label="Filtre" variant="selectable" icon="ri:filter-line" />
      </div>
    `}),parameters:{controls:{disable:!0}}},J={name:`Tailles`,render:()=>({components:{CspTag:L},setup(){return{sizes:W}},template:`
      <div class="flex flex-col gap-6">
        <div v-for="s in sizes" :key="s">
          <p class="mb-2 text-sm text-text-mention-grey">{{ s }}</p>
          <div class="flex flex-row gap-3 flex-wrap">
            <CspTag :label="'Étiquette ' + s" :size="s" variant="static" />
            <CspTag :label="'Lien ' + s" :size="s" variant="clickable" href="#" />
            <CspTag :label="'Filtre ' + s" :size="s" variant="selectable" />
            <CspTag :label="'Sélectionné ' + s" :size="s" variant="selectable" :pressed="true" />
            <CspTag :label="'Actif ' + s" :size="s" variant="dismissible" />
          </div>
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},Y={name:`Sélectionnable (autonome)`,render:()=>({components:{CspTag:L},setup(){return{a:l(!1),b:l(!0),c:l(!1)}},template:`
      <div class="flex flex-col gap-3">
        <p class="text-sm text-text-mention-grey">Tags <code>selectable</code> autonomes : chacun son <code>v-model:pressed</code>.</p>
        <div class="flex flex-row gap-2 flex-wrap">
          <CspTag label="Design" variant="selectable" v-model:pressed="a" />
          <CspTag label="Développement" variant="selectable" v-model:pressed="b" />
          <CspTag label="Produit" variant="selectable" v-model:pressed="c" />
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},X={name:`Sélectionnable (groupe)`,render:()=>({components:{CspTag:L,CspTagGroup:H},setup(){return{single:l(`dev`),multiple:l([`design`,`data`]),domains:[{value:`design`,label:`Design`},{value:`dev`,label:`Développement`},{value:`produit`,label:`Produit`},{value:`data`,label:`Data`}]}},template:`
    <p class="text-sm mb-2 text-text-mention-grey">(navigable avec les flèches directionnelles)</p>
      <div class="flex flex-col gap-6">
        <div class="flex flex-col gap-2">
          <p class="text-sm text-text-mention-grey">Groupe multiple</p>
          <CspTagGroup v-model="multiple" type="multiple">
            <CspTag
              v-for="d in domains"
              :key="d.value"
              :value="d.value"
              :label="d.label"
              variant="selectable"
            />
          </CspTagGroup>
        </div>
        <div class="flex flex-col gap-2">
          <p class="text-sm text-text-mention-grey">Groupe single</p>
          <CspTagGroup v-model="single" type="single">
            <CspTag
              v-for="d in domains"
              :key="d.value"
              :value="d.value"
              :label="d.label"
              variant="selectable"
            />
          </CspTagGroup>
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},Z={name:`Supprimable`,render:()=>({components:{CspTag:L},setup(){return{active:l([`Accessibilité`,`Vue`,`TypeScript`])}},template:`
      <div class="flex flex-col gap-3">
        <p class="text-sm text-text-mention-grey">Filtres actifs :</p>
        <div class="flex flex-row gap-2 flex-wrap">
          <CspTag
            v-for="label in active"
            :key="label"
            :label="label"
            variant="dismissible"
            @dismiss="active = active.filter(l => l !== label)"
          />
          <span v-if="active.length === 0" class="text-sm text-text-mention-grey italic">Aucun filtre actif</span>
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},Q={name:`États`,render:()=>({components:{CspTag:L},template:`
      <div class="flex flex-col gap-4">
        <div class="flex flex-row gap-3 flex-wrap items-center">
          <p class="w-28 text-sm text-text-mention-grey">Normal</p>
          <CspTag label="Clickable" variant="clickable" href="#" />
          <CspTag label="Sélectionnable" variant="selectable" />
          <CspTag label="Sélectionné" variant="selectable" :pressed="true" />
          <CspTag label="Actif" variant="dismissible" />
        </div>
        <div class="flex flex-row gap-3 flex-wrap items-center">
          <p class="w-28 text-sm text-text-mention-grey">Désactivé</p>
          <CspTag label="Clickable" variant="clickable" :disabled="true" />
          <CspTag label="Sélectionnable" variant="selectable" :disabled="true" />
          <CspTag label="Sélectionné" variant="selectable" :pressed="true" :disabled="true" />
          <CspTag label="Supprimable" variant="dismissible" :disabled="true" />
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},G.parameters={...G.parameters,docs:{...G.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...G.parameters?.docs?.source}}},K.parameters={...K.parameters,docs:{...K.parameters?.docs,source:{originalSource:`{
  name: 'Variantes',
  render: () => ({
    components: {
      CspTag
    },
    setup() {
      const pressed = ref(false);
      const dismissed = ref(false);
      return {
        pressed,
        dismissed
      };
    },
    template: \`
      <div class="flex flex-col gap-6">
        <div>
          <p class="mb-2 text-sm text-text-mention-grey">static (étiquette)</p>
          <CspTag label="Catégorie" variant="static" />
        </div>
        <div>
          <p class="mb-2 text-sm text-text-mention-grey">clickable (lien)</p>
          <CspTag label="Voir tout" variant="clickable" href="#" />
        </div>
        <div>
          <p class="mb-2 text-sm text-text-mention-grey">selectable (filtre à bascule / {{ pressed ? 'actif' : 'inactif' }})</p>
          <CspTag label="Filtre A" variant="selectable" v-model:pressed="pressed" />
        </div>
        <div>
          <p class="mb-2 text-sm text-text-mention-grey">dismissible : filtre actif à retirer</p>
          <CspTag v-if="!dismissed" label="Filtre actif" variant="dismissible" @dismiss="dismissed = true" />
          <span v-else class="text-sm text-text-mention-grey italic">retiré</span>
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...K.parameters?.docs?.source}}},q.parameters={...q.parameters,docs:{...q.parameters?.docs,source:{originalSource:`{
  name: 'Avec icône',
  render: () => ({
    components: {
      CspTag
    },
    template: \`
      <div class="flex flex-row gap-4 flex-wrap">
        <CspTag label="Étiquette" variant="static" icon="ri:bookmark-line" />
        <CspTag label="Lien" variant="clickable" icon="ri:external-link-line" href="#" />
        <CspTag label="Filtre" variant="selectable" icon="ri:filter-line" />
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...q.parameters?.docs?.source}}},J.parameters={...J.parameters,docs:{...J.parameters?.docs,source:{originalSource:`{
  name: 'Tailles',
  render: () => ({
    components: {
      CspTag
    },
    setup() {
      return {
        sizes: SIZES
      };
    },
    template: \`
      <div class="flex flex-col gap-6">
        <div v-for="s in sizes" :key="s">
          <p class="mb-2 text-sm text-text-mention-grey">{{ s }}</p>
          <div class="flex flex-row gap-3 flex-wrap">
            <CspTag :label="'Étiquette ' + s" :size="s" variant="static" />
            <CspTag :label="'Lien ' + s" :size="s" variant="clickable" href="#" />
            <CspTag :label="'Filtre ' + s" :size="s" variant="selectable" />
            <CspTag :label="'Sélectionné ' + s" :size="s" variant="selectable" :pressed="true" />
            <CspTag :label="'Actif ' + s" :size="s" variant="dismissible" />
          </div>
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...J.parameters?.docs?.source}}},Y.parameters={...Y.parameters,docs:{...Y.parameters?.docs,source:{originalSource:`{
  name: 'Sélectionnable (autonome)',
  render: () => ({
    components: {
      CspTag
    },
    setup() {
      const a = ref(false);
      const b = ref(true);
      const c = ref(false);
      return {
        a,
        b,
        c
      };
    },
    template: \`
      <div class="flex flex-col gap-3">
        <p class="text-sm text-text-mention-grey">Tags <code>selectable</code> autonomes : chacun son <code>v-model:pressed</code>.</p>
        <div class="flex flex-row gap-2 flex-wrap">
          <CspTag label="Design" variant="selectable" v-model:pressed="a" />
          <CspTag label="Développement" variant="selectable" v-model:pressed="b" />
          <CspTag label="Produit" variant="selectable" v-model:pressed="c" />
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...Y.parameters?.docs?.source}}},X.parameters={...X.parameters,docs:{...X.parameters?.docs,source:{originalSource:`{
  name: 'Sélectionnable (groupe)',
  render: () => ({
    components: {
      CspTag,
      CspTagGroup
    },
    setup() {
      const single = ref<string>('dev');
      const multiple = ref<string[]>(['design', 'data']);
      const domains = [{
        value: 'design',
        label: 'Design'
      }, {
        value: 'dev',
        label: 'Développement'
      }, {
        value: 'produit',
        label: 'Produit'
      }, {
        value: 'data',
        label: 'Data'
      }];
      return {
        single,
        multiple,
        domains
      };
    },
    template: \`
    <p class="text-sm mb-2 text-text-mention-grey">(navigable avec les flèches directionnelles)</p>
      <div class="flex flex-col gap-6">
        <div class="flex flex-col gap-2">
          <p class="text-sm text-text-mention-grey">Groupe multiple</p>
          <CspTagGroup v-model="multiple" type="multiple">
            <CspTag
              v-for="d in domains"
              :key="d.value"
              :value="d.value"
              :label="d.label"
              variant="selectable"
            />
          </CspTagGroup>
        </div>
        <div class="flex flex-col gap-2">
          <p class="text-sm text-text-mention-grey">Groupe single</p>
          <CspTagGroup v-model="single" type="single">
            <CspTag
              v-for="d in domains"
              :key="d.value"
              :value="d.value"
              :label="d.label"
              variant="selectable"
            />
          </CspTagGroup>
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...X.parameters?.docs?.source}}},Z.parameters={...Z.parameters,docs:{...Z.parameters?.docs,source:{originalSource:`{
  name: 'Supprimable',
  render: () => ({
    components: {
      CspTag
    },
    setup() {
      const active = ref(['Accessibilité', 'Vue', 'TypeScript']);
      return {
        active
      };
    },
    template: \`
      <div class="flex flex-col gap-3">
        <p class="text-sm text-text-mention-grey">Filtres actifs :</p>
        <div class="flex flex-row gap-2 flex-wrap">
          <CspTag
            v-for="label in active"
            :key="label"
            :label="label"
            variant="dismissible"
            @dismiss="active = active.filter(l => l !== label)"
          />
          <span v-if="active.length === 0" class="text-sm text-text-mention-grey italic">Aucun filtre actif</span>
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...Z.parameters?.docs?.source}}},Q.parameters={...Q.parameters,docs:{...Q.parameters?.docs,source:{originalSource:`{
  name: 'États',
  render: () => ({
    components: {
      CspTag
    },
    template: \`
      <div class="flex flex-col gap-4">
        <div class="flex flex-row gap-3 flex-wrap items-center">
          <p class="w-28 text-sm text-text-mention-grey">Normal</p>
          <CspTag label="Clickable" variant="clickable" href="#" />
          <CspTag label="Sélectionnable" variant="selectable" />
          <CspTag label="Sélectionné" variant="selectable" :pressed="true" />
          <CspTag label="Actif" variant="dismissible" />
        </div>
        <div class="flex flex-row gap-3 flex-wrap items-center">
          <p class="w-28 text-sm text-text-mention-grey">Désactivé</p>
          <CspTag label="Clickable" variant="clickable" :disabled="true" />
          <CspTag label="Sélectionnable" variant="selectable" :disabled="true" />
          <CspTag label="Sélectionné" variant="selectable" :pressed="true" :disabled="true" />
          <CspTag label="Supprimable" variant="dismissible" :disabled="true" />
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...Q.parameters?.docs?.source}}},$=[`Default`,`Variants`,`WithIcon`,`Sizes`,`Selectable`,`SelectableGroup`,`Dismissible`,`States`]}))();export{G as Default,Z as Dismissible,Y as Selectable,X as SelectableGroup,J as Sizes,Q as States,K as Variants,q as WithIcon,$ as __namedExportsOrder,U as default};