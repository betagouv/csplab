import{b as c,l as q,_ as Ve,K as m,f as g,ab as y,j as me,a1 as s,Q as L,g as G,R as D,y as N,B as _e,p as Ie,r as ze,L as Ge,a4 as ge,x as E,i as Le,W as Fe,O as b}from"./vue.esm-bundler-7zVN4DZj.js";import{P as v}from"./Primitive-DzgJnGz8.js";import{u as be}from"./useFormControl-5LFzebFo.js";import{q as fe,a as Ne,l as P}from"./useForwardExpose-qwf_wVRM.js";import{V as he}from"./VisuallyHiddenInput-CPKKsE9z.js";import{a as Ee}from"./Collection-C9Lj7FBv.js";import{i as ve}from"./isValueEqualOrExist-DvmIGGK4.js";import{i as B}from"./ohash.D__AXeF1-Cq3NGnZa.js";import{R as De}from"./RovingFocusGroup-DzvvbqBY.js";import{R as Pe}from"./RovingFocusItem-DT9Z5IoK.js";import{_ as j}from"./CspIcon-ClPxlQGO.js";import{_ as ye}from"./_plugin-vue_export-helper-DlAUqK2U.js";import"./usePrimitiveElement-BQ6g5-es.js";import"./VisuallyHidden-BOK6EsXA.js";import"./ConfigProvider-lmrMonQJ.js";import"./nullish-CHIgUVhi.js";import"./useId-Blg3GNwK.js";import"./iconify-DRloO12f.js";function Me({type:e,defaultValue:a,modelValue:t}){const i=t||a;return t!==void 0||a!==void 0?Array.isArray(i)?"multiple":"single":e??"single"}function Be({type:e,defaultValue:a,modelValue:t}){return e||Me({type:e,defaultValue:a,modelValue:t})}function je({type:e,defaultValue:a}){return a!==void 0?a:e==="single"?void 0:[]}function Oe(e,a){const t=c(()=>Be(e)),i=fe(e,"modelValue",a,{defaultValue:je(e),passive:e.modelValue===void 0,deep:!0});function n(r){if(t.value==="single")i.value=B(r,i.value)?void 0:r;else{const l=Array.isArray(i.value)?[...i.value||[]]:[i.value].filter(Boolean);if(ve(l,r)){const p=l.findIndex(h=>B(h,r));l.splice(p,1)}else l.push(r);i.value=l}}const d=c(()=>t.value==="single");return{modelValue:i,changeModelValue:n,isSingle:d}}const[xe,He]=Ne("ToggleGroupRoot");var Ue=q({__name:"ToggleGroupRoot",props:{rovingFocus:{type:Boolean,required:!1,default:!0},disabled:{type:Boolean,required:!1,default:!1},orientation:{type:String,required:!1},dir:{type:String,required:!1},loop:{type:Boolean,required:!1,default:!0},asChild:{type:Boolean,required:!1},as:{type:null,required:!1},name:{type:String,required:!1},required:{type:Boolean,required:!1},type:{type:String,required:!1},modelValue:{type:null,required:!1},defaultValue:{type:null,required:!1}},emits:["update:modelValue"],setup(e,{emit:a}){const t=e,i=a,{loop:n,rovingFocus:d,disabled:r,dir:l}=Ve(t),p=Ee(l),{forwardRef:h,currentElement:x}=P(),{modelValue:o,changeModelValue:T,isSingle:C}=Oe(t,i),k=be(x);return He({isSingle:C,modelValue:o,changeModelValue:T,dir:p,orientation:t.orientation,loop:n,rovingFocus:d,disabled:r}),(u,F)=>(m(),g(D(s(d)?s(De):s(v)),{"as-child":"",orientation:s(d)?u.orientation:void 0,dir:s(p),loop:s(d)?s(n):void 0},{default:y(()=>[me(s(v),{ref:s(h),role:"group","as-child":u.asChild,as:u.as},{default:y(()=>[L(u.$slots,"default",{modelValue:s(o)}),s(k)&&u.name?(m(),g(he,{key:0,name:u.name,required:u.required,value:s(o)},null,8,["name","required","value"])):G("v-if",!0)]),_:3},8,["as-child","as"])]),_:3},8,["orientation","dir","loop"]))}}),Ke=Ue,$e=q({__name:"Toggle",props:{defaultValue:{type:Boolean,required:!1},modelValue:{type:[Boolean,null],required:!1,default:void 0},disabled:{type:Boolean,required:!1,default:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:"button"},name:{type:String,required:!1},required:{type:Boolean,required:!1}},emits:["update:modelValue"],setup(e,{emit:a}){const t=e,i=a,{forwardRef:n,currentElement:d}=P(),r=xe(null),l=fe(t,"modelValue",i,{defaultValue:t.defaultValue,passive:t.modelValue===void 0});function p(){l.value=!l.value}const h=c(()=>l.value?"on":"off"),x=be(d);return(o,T)=>(m(),g(s(v),{ref:s(n),type:o.as==="button"?"button":void 0,"as-child":t.asChild,as:o.as,"aria-pressed":s(l),"data-state":h.value,"data-disabled":o.disabled?"":void 0,disabled:o.disabled,onClick:p},{default:y(()=>[L(o.$slots,"default",{modelValue:s(l),disabled:o.disabled,pressed:s(l),state:h.value}),s(x)&&o.name&&!s(r)?(m(),g(he,{key:0,type:"checkbox",name:o.name,value:s(l),required:o.required},null,8,["name","value","required"])):G("v-if",!0)]),_:3},8,["type","as-child","as","aria-pressed","data-state","data-disabled","disabled"]))}}),Te=$e,We=q({__name:"ToggleGroupItem",props:{value:{type:null,required:!0},disabled:{type:Boolean,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:"button"}},setup(e){const a=e,t=xe(),i=c(()=>{var r;return((r=t.disabled)==null?void 0:r.value)||a.disabled}),n=c(()=>ve(t.modelValue.value,a.value)),{forwardRef:d}=P();return(r,l)=>(m(),g(D(s(t).rovingFocus.value?s(Pe):s(v)),N({"as-child":""},s(t).rovingFocus.value?{focusable:!i.value,active:n.value}:{}),{default:y(()=>[me(s(Te),N(a,{ref:s(d),disabled:i.value,"model-value":n.value,"onUpdate:modelValue":l[0]||(l[0]=p=>s(t).changeModelValue(r.value))}),{default:y(p=>[L(r.$slots,"default",_e(Ie(p)))]),_:3},16,["disabled","model-value"])]),_:3},16))}}),Ze=We;function Ce(e){switch(e.variant){case"selectable":return e.inGroup?"toggle-group-item":"toggle";case"clickable":return e.hasHref&&!e.disabled?"a":"button";case"dismissible":return"button";case"static":return"p";default:return"p"}}function ke(e,a){return e||(a?`Retirer le filtre ${a}`:void 0)}Ce.__docgenInfo={exportName:"resolveTagRoot",displayName:"resolveTagRoot",type:2,props:[{name:"variant",global:!1,description:"",tags:[],required:!0,type:"CspTagVariant",declarations:[],schema:{kind:"enum",type:"CspTagVariant",schema:['"static"','"clickable"','"selectable"','"dismissible"']}},{name:"inGroup",global:!1,description:"",tags:[],required:!0,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"disabled",global:!1,description:"",tags:[],required:!0,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"hasHref",global:!1,description:"",tags:[],required:!0,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}}],events:[],slots:[],exposed:[],sourceFiles:"/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspTag/tag.ts"};ke.__docgenInfo={exportName:"resolveDismissAriaLabel",displayName:"resolveDismissAriaLabel",type:2,props:[{name:"toString",global:!1,description:"Returns a string representation of a string.",tags:[],required:!0,type:"() => string",declarations:[],schema:{kind:"event",type:"(): string"}},{name:"charAt",global:!1,description:"Returns the character at the specified index.",tags:[{name:"param",text:"pos The zero-based index of the desired character."}],required:!0,type:"(pos: number) => string",declarations:[],schema:{kind:"event",type:"(pos: number): string"}},{name:"charCodeAt",global:!1,description:"Returns the Unicode value of the character at the specified location.",tags:[{name:"param",text:"index The zero-based index of the desired character. If there is no character at the specified index, NaN is returned."}],required:!0,type:"(index: number) => number",declarations:[],schema:{kind:"event",type:"(index: number): number"}},{name:"concat",global:!1,description:"Returns a string that contains the concatenation of two or more strings.",tags:[{name:"param",text:"strings The strings to append to the end of the string."}],required:!0,type:"(...strings: string[]) => string",declarations:[],schema:{kind:"event",type:"(...strings: string[]): string"}},{name:"indexOf",global:!1,description:"Returns the position of the first occurrence of a substring.",tags:[{name:"param",text:"searchString The substring to search for in the string"},{name:"param",text:"position The index at which to begin searching the String object. If omitted, search starts at the beginning of the string."}],required:!0,type:"(searchString: string, position?: number) => number",declarations:[],schema:{kind:"event",type:"(searchString: string, position?: number): number"}},{name:"lastIndexOf",global:!1,description:"Returns the last occurrence of a substring in the string.",tags:[{name:"param",text:"searchString The substring to search for."},{name:"param",text:"position The index at which to begin searching. If omitted, the search begins at the end of the string."}],required:!0,type:"(searchString: string, position?: number) => number",declarations:[],schema:{kind:"event",type:"(searchString: string, position?: number): number"}},{name:"localeCompare",global:!1,description:`Determines whether two strings are equivalent in the current locale.
Determines whether two strings are equivalent in the current or specified locale.`,tags:[{name:"param",text:"that String to compare to target string"},{name:"param",text:"that String to compare to target string"},{name:"param",text:"locales A locale string or array of locale strings that contain one or more language or locale tags. If you include more than one locale string, list them in descending order of priority so that the first entry is the preferred locale. If you omit this parameter, the default locale of the JavaScript runtime is used. This parameter must conform to BCP 47 standards; see the Intl.Collator object for details."},{name:"param",text:"options An object that contains one or more properties that specify comparison options. see the Intl.Collator object for details."},{name:"param",text:"that String to compare to target string"},{name:"param",text:"locales A locale string or array of locale strings that contain one or more language or locale tags. If you include more than one locale string, list them in descending order of priority so that the first entry is the preferred locale. If you omit this parameter, the default locale of the JavaScript runtime is used. This parameter must conform to BCP 47 standards; see the Intl.Collator object for details."},{name:"param",text:"options An object that contains one or more properties that specify comparison options. see the Intl.Collator object for details."}],required:!0,type:"{ (that: string): number; (that: string, locales?: string | string[], options?: CollatorOptions): number; (that: string, locales?: LocalesArgument, options?: CollatorOptions): number; }",declarations:[],schema:"{ (that: string): number; (that: string, locales?: string | string[], options?: CollatorOptions): number; (that: string, locales?: LocalesArgument, options?: CollatorOptions): number; }"},{name:"match",global:!1,description:`Matches a string with a regular expression, and returns an array containing the results of that search.
Matches a string or an object that supports being matched against, and returns an array
containing the results of that search, or null if no matches are found.`,tags:[{name:"param",text:"regexp A variable name or string literal containing the regular expression pattern and flags."},{name:"param",text:"matcher An object that supports being matched against."}],required:!0,type:"{ (regexp: string | RegExp): RegExpMatchArray; (matcher: { [Symbol.match](string: string): RegExpMatchArray; }): RegExpMatchArray; }",declarations:[],schema:"{ (regexp: string | RegExp): RegExpMatchArray; (matcher: { [Symbol.match](string: string): RegExpMatchArray; }): RegExpMatchArray; }"},{name:"replace",global:!1,description:"Replaces text in a string, using a regular expression or search string.\nPasses a string and {@linkcode replaceValue} to the `[Symbol.replace]` method on {@linkcode searchValue}. This method is expected to implement its own replacement algorithm.\nReplaces text in a string, using an object that supports replacement within a string.",tags:[{name:"param",text:"searchValue A string or regular expression to search for."},{name:"param",text:"replaceValue A string containing the text to replace. When the {@linkcode searchValue} is a `RegExp`, all matches are replaced if the `g` flag is set (or only those matches at the beginning, if the `y` flag is also present). Otherwise, only the first match of {@linkcode searchValue} is replaced."},{name:"param",text:"searchValue A string to search for."},{name:"param",text:"replacer A function that returns the replacement text."},{name:"param",text:"searchValue An object that supports searching for and replacing matches within a string."},{name:"param",text:"replaceValue The replacement text."},{name:"param",text:"searchValue A object can search for and replace matches within a string."},{name:"param",text:"replacer A function that returns the replacement text."}],required:!0,type:"{ (searchValue: string | RegExp, replaceValue: string): string; (searchValue: string | RegExp, replacer: (substring: string, ...args: any[]) => string): string; (searchValue: { ...; }, replaceValue: string): string; (searchValue: { ...; }, replacer: (substring: string, ...args: any[]) => string): string; }",declarations:[],schema:"{ (searchValue: string | RegExp, replaceValue: string): string; (searchValue: string | RegExp, replacer: (substring: string, ...args: any[]) => string): string; (searchValue: { ...; }, replaceValue: string): string; (searchValue: { ...; }, replacer: (substring: string, ...args: any[]) => string): string; }"},{name:"search",global:!1,description:"Finds the first substring match in a regular expression search.",tags:[{name:"param",text:"regexp The regular expression pattern and applicable flags."},{name:"param",text:"searcher An object which supports searching within a string."}],required:!0,type:"{ (regexp: string | RegExp): number; (searcher: { [Symbol.search](string: string): number; }): number; }",declarations:[],schema:"{ (regexp: string | RegExp): number; (searcher: { [Symbol.search](string: string): number; }): number; }"},{name:"slice",global:!1,description:"Returns a section of a string.",tags:[{name:"param",text:"start The index to the beginning of the specified portion of stringObj."},{name:"param",text:`end The index to the end of the specified portion of stringObj. The substring includes the characters up to, but not including, the character indicated by end.
If this value is not specified, the substring continues to the end of stringObj.`}],required:!0,type:"(start?: number, end?: number) => string",declarations:[],schema:{kind:"event",type:"(start?: number, end?: number): string"}},{name:"split",global:!1,description:"Split a string into substrings using the specified separator and return them as an array.",tags:[{name:"param",text:"separator A string that identifies character or characters to use in separating the string. If omitted, a single-element array containing the entire string is returned."},{name:"param",text:"limit A value used to limit the number of elements returned in the array."},{name:"param",text:"splitter An object that can split a string."},{name:"param",text:"limit A value used to limit the number of elements returned in the array."}],required:!0,type:"{ (separator: string | RegExp, limit?: number): string[]; (splitter: { [Symbol.split](string: string, limit?: number): string[]; }, limit?: number): string[]; }",declarations:[],schema:"{ (separator: string | RegExp, limit?: number): string[]; (splitter: { [Symbol.split](string: string, limit?: number): string[]; }, limit?: number): string[]; }"},{name:"substring",global:!1,description:"Returns the substring at the specified location within a String object.",tags:[{name:"param",text:"start The zero-based index number indicating the beginning of the substring."},{name:"param",text:`end Zero-based index number indicating the end of the substring. The substring includes the characters up to, but not including, the character indicated by end.
If end is omitted, the characters from start through the end of the original string are returned.`}],required:!0,type:"(start: number, end?: number) => string",declarations:[],schema:{kind:"event",type:"(start: number, end?: number): string"}},{name:"toLowerCase",global:!1,description:"Converts all the alphabetic characters in a string to lowercase.",tags:[],required:!0,type:"() => string",declarations:[],schema:{kind:"event",type:"(): string"}},{name:"toLocaleLowerCase",global:!1,description:"Converts all alphabetic characters to lowercase, taking into account the host environment's current locale.",tags:[],required:!0,type:"{ (locales?: string | string[]): string; (locales?: LocalesArgument): string; }",declarations:[],schema:"{ (locales?: string | string[]): string; (locales?: LocalesArgument): string; }"},{name:"toUpperCase",global:!1,description:"Converts all the alphabetic characters in a string to uppercase.",tags:[],required:!0,type:"() => string",declarations:[],schema:{kind:"event",type:"(): string"}},{name:"toLocaleUpperCase",global:!1,description:"Returns a string where all alphabetic characters have been converted to uppercase, taking into account the host environment's current locale.",tags:[],required:!0,type:"{ (locales?: string | string[]): string; (locales?: LocalesArgument): string; }",declarations:[],schema:"{ (locales?: string | string[]): string; (locales?: LocalesArgument): string; }"},{name:"trim",global:!1,description:"Removes the leading and trailing white space and line terminator characters from a string.",tags:[],required:!0,type:"() => string",declarations:[],schema:{kind:"event",type:"(): string"}},{name:"length",global:!1,description:"Returns the length of a String object.",tags:[],required:!0,type:"number",declarations:[],schema:"number"},{name:"substr",global:!1,description:"Gets a substring beginning at the specified location and having the specified length.",tags:[{name:"deprecated",text:"A legacy feature for browser compatibility"},{name:"param",text:"from The starting position of the desired substring. The index of the first character in the string is zero."},{name:"param",text:"length The number of characters to include in the returned substring."}],required:!0,type:"(from: number, length?: number) => string",declarations:[],schema:{kind:"event",type:"(from: number, length?: number): string"}},{name:"valueOf",global:!1,description:"Returns the primitive value of the specified object.",tags:[],required:!0,type:"() => string",declarations:[],schema:{kind:"event",type:"(): string"}},{name:"codePointAt",global:!1,description:`Returns a nonnegative integer Number less than 1114112 (0x110000) that is the code point
value of the UTF-16 encoded code point starting at the string element at position pos in
the String resulting from converting this object to a String.
If there is no element at that position, the result is undefined.
If a valid UTF-16 surrogate pair does not begin at pos, the result is the code unit at pos.`,tags:[],required:!0,type:"(pos: number) => number",declarations:[],schema:{kind:"event",type:"(pos: number): number"}},{name:"includes",global:!1,description:`Returns true if searchString appears as a substring of the result of converting this
object to a String, at one or more positions that are
greater than or equal to position; otherwise, returns false.`,tags:[{name:"param",text:"searchString search string"},{name:"param",text:"position If position is undefined, 0 is assumed, so as to search all of the String."}],required:!0,type:"(searchString: string, position?: number) => boolean",declarations:[],schema:{kind:"event",type:"(searchString: string, position?: number): boolean"}},{name:"endsWith",global:!1,description:`Returns true if the sequence of elements of searchString converted to a String is the
same as the corresponding elements of this object (converted to a String) starting at
endPosition – length(this). Otherwise returns false.`,tags:[],required:!0,type:"(searchString: string, endPosition?: number) => boolean",declarations:[],schema:{kind:"event",type:"(searchString: string, endPosition?: number): boolean"}},{name:"normalize",global:!1,description:`Returns the String value result of normalizing the string into the normalization form
named by form as specified in Unicode Standard Annex #15, Unicode Normalization Forms.`,tags:[{name:"param",text:`form Applicable values: "NFC", "NFD", "NFKC", or "NFKD", If not specified default
is "NFC"`},{name:"param",text:`form Applicable values: "NFC", "NFD", "NFKC", or "NFKD", If not specified default
is "NFC"`}],required:!0,type:'{ (form: "NFC" | "NFD" | "NFKC" | "NFKD"): string; (form?: string): string; }',declarations:[],schema:'{ (form: "NFC" | "NFD" | "NFKC" | "NFKD"): string; (form?: string): string; }'},{name:"repeat",global:!1,description:`Returns a String value that is made from count copies appended together. If count is 0,
the empty string is returned.`,tags:[{name:"param",text:"count number of copies to append"}],required:!0,type:"(count: number) => string",declarations:[],schema:{kind:"event",type:"(count: number): string"}},{name:"startsWith",global:!1,description:`Returns true if the sequence of elements of searchString converted to a String is the
same as the corresponding elements of this object (converted to a String) starting at
position. Otherwise returns false.`,tags:[],required:!0,type:"(searchString: string, position?: number) => boolean",declarations:[],schema:{kind:"event",type:"(searchString: string, position?: number): boolean"}},{name:"anchor",global:!1,description:"Returns an `<a>` HTML anchor element and sets the name attribute to the text value",tags:[{name:"deprecated",text:"A legacy feature for browser compatibility"},{name:"param",text:"name"}],required:!0,type:"(name: string) => string",declarations:[],schema:{kind:"event",type:"(name: string): string"}},{name:"big",global:!1,description:"Returns a `<big>` HTML element",tags:[{name:"deprecated",text:"A legacy feature for browser compatibility"}],required:!0,type:"() => string",declarations:[],schema:{kind:"event",type:"(): string"}},{name:"blink",global:!1,description:"Returns a `<blink>` HTML element",tags:[{name:"deprecated",text:"A legacy feature for browser compatibility"}],required:!0,type:"() => string",declarations:[],schema:{kind:"event",type:"(): string"}},{name:"bold",global:!1,description:"Returns a `<b>` HTML element",tags:[{name:"deprecated",text:"A legacy feature for browser compatibility"}],required:!0,type:"() => string",declarations:[],schema:{kind:"event",type:"(): string"}},{name:"fixed",global:!1,description:"Returns a `<tt>` HTML element",tags:[{name:"deprecated",text:"A legacy feature for browser compatibility"}],required:!0,type:"() => string",declarations:[],schema:{kind:"event",type:"(): string"}},{name:"fontcolor",global:!1,description:"Returns a `<font>` HTML element and sets the color attribute value",tags:[{name:"deprecated",text:"A legacy feature for browser compatibility"}],required:!0,type:"(color: string) => string",declarations:[],schema:{kind:"event",type:"(color: string): string"}},{name:"fontsize",global:!1,description:"Returns a `<font>` HTML element and sets the size attribute value",tags:[{name:"deprecated",text:"A legacy feature for browser compatibility"},{name:"deprecated",text:"A legacy feature for browser compatibility"}],required:!0,type:"{ (size: number): string; (size: string): string; }",declarations:[],schema:"{ (size: number): string; (size: string): string; }"},{name:"italics",global:!1,description:"Returns an `<i>` HTML element",tags:[{name:"deprecated",text:"A legacy feature for browser compatibility"}],required:!0,type:"() => string",declarations:[],schema:{kind:"event",type:"(): string"}},{name:"link",global:!1,description:"Returns an `<a>` HTML element and sets the href attribute value",tags:[{name:"deprecated",text:"A legacy feature for browser compatibility"}],required:!0,type:"(url: string) => string",declarations:[],schema:{kind:"event",type:"(url: string): string"}},{name:"small",global:!1,description:"Returns a `<small>` HTML element",tags:[{name:"deprecated",text:"A legacy feature for browser compatibility"}],required:!0,type:"() => string",declarations:[],schema:{kind:"event",type:"(): string"}},{name:"strike",global:!1,description:"Returns a `<strike>` HTML element",tags:[{name:"deprecated",text:"A legacy feature for browser compatibility"}],required:!0,type:"() => string",declarations:[],schema:{kind:"event",type:"(): string"}},{name:"sub",global:!1,description:"Returns a `<sub>` HTML element",tags:[{name:"deprecated",text:"A legacy feature for browser compatibility"}],required:!0,type:"() => string",declarations:[],schema:{kind:"event",type:"(): string"}},{name:"sup",global:!1,description:"Returns a `<sup>` HTML element",tags:[{name:"deprecated",text:"A legacy feature for browser compatibility"}],required:!0,type:"() => string",declarations:[],schema:{kind:"event",type:"(): string"}},{name:"padStart",global:!1,description:`Pads the current string with a given string (possibly repeated) so that the resulting string reaches a given length.
The padding is applied from the start (left) of the current string.`,tags:[{name:"param",text:`maxLength The length of the resulting string once the current string has been padded.
If this parameter is smaller than the current string's length, the current string will be returned as it is.`},{name:"param",text:`fillString The string to pad the current string with.
If this string is too long, it will be truncated and the left-most part will be applied.
The default value for this parameter is " " (U+0020).`}],required:!0,type:"(maxLength: number, fillString?: string) => string",declarations:[],schema:{kind:"event",type:"(maxLength: number, fillString?: string): string"}},{name:"padEnd",global:!1,description:`Pads the current string with a given string (possibly repeated) so that the resulting string reaches a given length.
The padding is applied from the end (right) of the current string.`,tags:[{name:"param",text:`maxLength The length of the resulting string once the current string has been padded.
If this parameter is smaller than the current string's length, the current string will be returned as it is.`},{name:"param",text:`fillString The string to pad the current string with.
If this string is too long, it will be truncated and the left-most part will be applied.
The default value for this parameter is " " (U+0020).`}],required:!0,type:"(maxLength: number, fillString?: string) => string",declarations:[],schema:{kind:"event",type:"(maxLength: number, fillString?: string): string"}},{name:"trimEnd",global:!1,description:"Removes the trailing white space and line terminator characters from a string.",tags:[],required:!0,type:"() => string",declarations:[],schema:{kind:"event",type:"(): string"}},{name:"trimStart",global:!1,description:"Removes the leading white space and line terminator characters from a string.",tags:[],required:!0,type:"() => string",declarations:[],schema:{kind:"event",type:"(): string"}},{name:"trimLeft",global:!1,description:"Removes the leading white space and line terminator characters from a string.",tags:[{name:"deprecated",text:"A legacy feature for browser compatibility. Use `trimStart` instead"}],required:!0,type:"() => string",declarations:[],schema:{kind:"event",type:"(): string"}},{name:"trimRight",global:!1,description:"Removes the trailing white space and line terminator characters from a string.",tags:[{name:"deprecated",text:"A legacy feature for browser compatibility. Use `trimEnd` instead"}],required:!0,type:"() => string",declarations:[],schema:{kind:"event",type:"(): string"}},{name:"matchAll",global:!1,description:`Matches a string with a regular expression, and returns an iterable of matches
containing the results of that search.`,tags:[{name:"param",text:"regexp A variable name or string literal containing the regular expression pattern and flags."}],required:!0,type:"(regexp: RegExp) => RegExpStringIterator<RegExpExecArray>",declarations:[],schema:{kind:"event",type:"(regexp: RegExp): RegExpStringIterator<RegExpExecArray>"}},{name:"__@iterator@369",global:!1,description:"Iterator",tags:[],required:!0,type:"() => StringIterator<string>",declarations:[],schema:{kind:"event",type:"(): StringIterator<string>"}}],events:[],slots:[],exposed:[],sourceFiles:"/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspTag/tag.ts"};const qe=Symbol("CspTagGroup");function Se(e){Ge(qe,e)}function Je(){return ze(qe,null)}Se.__docgenInfo={exportName:"provideCspTagGroup",displayName:"provideCspTagGroup",type:2,props:[{name:"size",global:!1,description:"",tags:[],required:!1,type:"CspTagSize",declarations:[],schema:{kind:"enum",type:"CspTagSize",schema:['"md"','"sm"','"lg"']}},{name:"disabled",global:!1,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}}],events:[],slots:[],exposed:[],sourceFiles:"/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspTag/useCspTagGroup.ts"};const we=q({__name:"CspTag",props:E({size:{},label:{},disabled:{type:Boolean},icon:{},as:{},asChild:{type:Boolean},variant:{},href:{},value:{},dismissLabel:{}},{pressed:{type:Boolean,default:!1},pressedModifiers:{}}),emits:E(["dismiss"],["update:pressed"]),setup(e,{emit:a}){const t=e,i=a,n=c(()=>t.variant??"static"),d=ge(e,"pressed"),r=Je(),l=c(()=>t.size??(r==null?void 0:r.size)??"md"),p=c(()=>t.disabled??(r==null?void 0:r.disabled)??!1),h=c(()=>n.value!=="static"&&n.value!=="dismissible"),x=c(()=>n.value==="selectable"&&r!==null),o=c(()=>"icon"in t?t.icon:void 0),T=c(()=>"href"in t?t.href:void 0),C=c(()=>"as"in t?t.as:void 0),k=c(()=>"asChild"in t?t.asChild:void 0),u=c(()=>ke("dismissLabel"in t?t.dismissLabel:void 0,t.label)),F=c(()=>{switch(Ce({variant:n.value,inGroup:x.value,disabled:p.value,hasHref:!!T.value})){case"toggle-group-item":return{is:Ze,attrs:{value:"value"in t?t.value:void 0,disabled:p.value}};case"toggle":return{is:Te,attrs:{modelValue:d.value,"onUpdate:modelValue":M=>{d.value=M},disabled:p.value}};case"a":return{is:v,attrs:{as:C.value??"a",asChild:k.value,href:T.value}};case"button":return{is:v,attrs:n.value==="dismissible"?{as:"button",type:"button",disabled:p.value,"aria-label":u.value,onClick:()=>i("dismiss")}:{as:C.value??"button",asChild:k.value,type:"button",disabled:p.value}};case"p":default:return{is:v,attrs:{as:C.value??"p",asChild:k.value}}}});return(Ae,M)=>(m(),g(D(F.value.is),N(F.value.attrs,{class:["csp-tag",[`csp-tag--${l.value}`,{"csp-tag--interactive":h.value,"csp-tag--dismissible":n.value==="dismissible"}]]}),{default:y(()=>[o.value?(m(),g(j,{key:0,class:"csp-tag__icon",name:o.value,"aria-hidden":"true"},null,8,["name"])):G("",!0),Le(" "+Fe(e.label)+" ",1),n.value==="dismissible"?(m(),g(j,{key:1,class:"csp-tag__dismiss",name:"ri:close-line","aria-hidden":"true"})):G("",!0)]),_:1},16,["class"]))}}),f=ye(we,[["__scopeId","data-v-49d39347"]]);we.__docgenInfo={exportName:"default",displayName:"CspTag",type:1,props:[{name:"key",global:!0,description:"",tags:[],required:!1,type:"PropertyKey",declarations:[],schema:{kind:"enum",type:"PropertyKey",schema:["string","number","symbol"]}},{name:"ref",global:!0,description:"",tags:[],required:!1,type:"VNodeRef",declarations:[],schema:{kind:"enum",type:"VNodeRef",schema:["string","Ref<any, any>",{kind:"event",type:"(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void"}]}},{name:"ref_for",global:!0,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"ref_key",global:!0,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"class",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"},{name:"style",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"},{name:"size",global:!1,description:"",tags:[],required:!1,type:"CspTagSize",declarations:[],schema:{kind:"enum",type:"CspTagSize",schema:['"md"','"sm"','"lg"']}},{name:"variant",global:!1,description:"",tags:[],required:!1,type:'"static" | "clickable" | "selectable" | "dismissible"',declarations:[],schema:{kind:"enum",type:'"static" | "clickable" | "selectable" | "dismissible"',schema:['"static"','"clickable"','"selectable"','"dismissible"']}},{name:"disabled",global:!1,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"label",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"pressed",global:!1,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]},default:"false"}],events:[{name:"update:pressed",description:"",tags:[],type:"[value: boolean]",signature:'(event: "update:pressed", value: boolean): void',declarations:[],schema:[{kind:"enum",type:"boolean",schema:["false","true"]}]},{name:"dismiss",description:"",tags:[],type:"[]",signature:'(event: "dismiss"): void',declarations:[],schema:[]}],slots:[],exposed:[{name:"size",type:"CspTagSize",description:"",declarations:[],schema:{kind:"enum",type:"CspTagSize",schema:['"md"','"sm"','"lg"']}},{name:"variant",type:'"static" | "clickable" | "selectable" | "dismissible"',description:"",declarations:[],schema:{kind:"enum",type:'"static" | "clickable" | "selectable" | "dismissible"',schema:['"static"','"clickable"','"selectable"','"dismissible"']}},{name:"disabled",type:"boolean",description:"",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"label",type:"string",description:"",declarations:[],schema:"string"},{name:"pressed",type:"boolean",description:"",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}}],sourceFiles:"/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspTag/CspTag.vue"};const Re=q({__name:"CspTagGroup",props:E({type:{default:"multiple"},size:{},disabled:{type:Boolean,default:!1},loop:{type:Boolean,default:!0}},{modelValue:{},modelModifiers:{}}),emits:["update:modelValue"],setup(e){const a=e,t=ge(e,"modelValue");return Se({size:a.size,disabled:a.disabled}),(i,n)=>(m(),g(s(Ke),{modelValue:t.value,"onUpdate:modelValue":n[0]||(n[0]=d=>t.value=d),class:"csp-tag-group",type:e.type,disabled:e.disabled,loop:e.loop,"roving-focus":!0},{default:y(()=>[L(i.$slots,"default",{},void 0,!0)]),_:3},8,["modelValue","type","disabled","loop"]))}}),Qe=ye(Re,[["__scopeId","data-v-53ec5618"]]);Re.__docgenInfo={exportName:"default",displayName:"CspTagGroup",type:2,props:[{name:"type",global:!1,description:"",tags:[],required:!1,type:'"single" | "multiple"',declarations:[],schema:{kind:"enum",type:'"single" | "multiple"',schema:['"single"','"multiple"']},default:'"multiple"'},{name:"size",global:!1,description:"",tags:[],required:!1,type:"CspTagSize",declarations:[],schema:{kind:"enum",type:"CspTagSize",schema:['"md"','"sm"','"lg"']}},{name:"disabled",global:!1,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]},default:"false"},{name:"loop",global:!1,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]},default:"true"},{name:"modelValue",global:!1,description:"",tags:[],required:!1,type:"string | number | (string | number)[]",declarations:[],schema:{kind:"enum",type:"string | number | (string | number)[]",schema:["string","number",{kind:"array",type:"(string | number)[]"}]}},{name:"key",global:!0,description:"",tags:[],required:!1,type:"PropertyKey",declarations:[],schema:{kind:"enum",type:"PropertyKey",schema:["string","number","symbol"]}},{name:"ref",global:!0,description:"",tags:[],required:!1,type:"VNodeRef",declarations:[],schema:{kind:"enum",type:"VNodeRef",schema:["string","Ref<any, any>",{kind:"event",type:"(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void"}]}},{name:"ref_for",global:!0,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"ref_key",global:!0,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"class",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"},{name:"style",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"}],events:[{name:"update:modelValue",description:"",tags:[],type:"[value: string | number | (string | number)[]]",signature:'(evt: "update:modelValue", value: string | number | (string | number)[]): void',declarations:[],schema:[{kind:"enum",type:"string | number | (string | number)[]",schema:["string","number",{kind:"array",type:"(string | number)[]"}]}]}],slots:[{name:"default",type:"{}",description:"",declarations:[],schema:{kind:"object",type:"{}"}}],exposed:[],sourceFiles:"/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspTag/CspTagGroup.vue"};const ht={title:"Éléments/Génériques/CspTag",component:f,tags:["autodocs"],parameters:{controls:{include:["label","variant","size","icon","pressed","disabled","href","value","dismissLabel"]},docs:{description:{component:"Étiquette générique. Sert à **catégoriser ou filtrer** les contenus (à ne pas confondre avec `CspBadge` qui signale un état).\n\nConstruit sur les primitives [reka-ui](https://reka-ui.com) :\n- `static` et `clickable` reposent sur le composant `Primitive` de reka et sont polymorphes via `as` / `asChild` ;\n- `dismissible` est toujours un `<button>` ;\n- `selectable` repose sur le composant reka `Toggle` rendu seul, ou sur `ToggleGroupItem` lorsqu'il est placé dans un `CspTagGroup`.\n"}}},argTypes:{label:{control:{type:"text"},description:"Libellé du tag (cas simple). Pour un contenu riche, utiliser le slot par défaut.",table:{type:{summary:"string"}}},variant:{control:{type:"radio"},options:["static","clickable","selectable","dismissible"],description:"Mode d'interaction du tag.",table:{type:{summary:"static | clickable | selectable | dismissible"},defaultValue:{summary:"static"}}},size:{control:{type:"radio"},options:["sm","md","lg"],description:"Taille du tag. Héritée du `CspTagGroup` si non précisée.",table:{type:{summary:"sm | md | lg"},defaultValue:{summary:"md"}}},icon:{control:{type:"text"},description:"Icône Iconify affichée à gauche. Non disponible sur `dismissible` (croix exclusive).",table:{type:{summary:"string"}}},pressed:{control:{type:"boolean"},description:"État activé du tag `selectable` autonome. Lier avec `v-model:pressed`.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},disabled:{control:{type:"boolean"},description:"Désactive les variantes interactives. Héritée du `CspTagGroup`.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},href:{control:{type:"text"},description:"URL cible pour la variante `clickable`. Rend un `<a>` si fourni, sinon un `<button>`.",table:{type:{summary:"string"}}},value:{control:{type:"text"},description:"Identifiant d'un tag `selectable` au sein d'un `CspTagGroup`.",table:{type:{summary:"string | number"}}},dismissLabel:{control:{type:"text"},description:"Label accessible du bouton de suppression (`dismissible`). Par défaut : `Retirer le filtre {label}`.",table:{type:{summary:"string"}}},as:{control:!1,table:{disable:!0}},asChild:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{label:"Libellé",variant:"static",size:"md",pressed:!1,disabled:!1},render:e=>({components:{CspTag:f},setup(){const a=b(!!e.pressed);return{args:e,pressed:a}},template:`
      <CspTag
        v-bind="args"
        v-model:pressed="pressed"
        @dismiss="() => {}"
      />
    `})},Ye=["sm","md","lg"],S={name:"Par défaut"},w={name:"Variantes",render:()=>({components:{CspTag:f},setup(){const e=b(!1),a=b(!1);return{pressed:e,dismissed:a}},template:`
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
    `}),parameters:{controls:{disable:!0}}},R={name:"Avec icône",render:()=>({components:{CspTag:f},template:`
      <div class="flex flex-row gap-4 flex-wrap">
        <CspTag label="Étiquette" variant="static" icon="ri:bookmark-line" />
        <CspTag label="Lien" variant="clickable" icon="ri:external-link-line" href="#" />
        <CspTag label="Filtre" variant="selectable" icon="ri:filter-line" />
      </div>
    `}),parameters:{controls:{disable:!0}}},A={name:"Tailles",render:()=>({components:{CspTag:f},setup(){return{sizes:Ye}},template:`
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
    `}),parameters:{controls:{disable:!0}}},V={name:"Sélectionnable (autonome)",render:()=>({components:{CspTag:f},setup(){const e=b(!1),a=b(!0),t=b(!1);return{a:e,b:a,c:t}},template:`
      <div class="flex flex-col gap-3">
        <p class="text-sm text-text-mention-grey">Tags <code>selectable</code> autonomes : chacun son <code>v-model:pressed</code>.</p>
        <div class="flex flex-row gap-2 flex-wrap">
          <CspTag label="Design" variant="selectable" v-model:pressed="a" />
          <CspTag label="Développement" variant="selectable" v-model:pressed="b" />
          <CspTag label="Produit" variant="selectable" v-model:pressed="c" />
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},_={name:"Sélectionnable (groupe)",render:()=>({components:{CspTag:f,CspTagGroup:Qe},setup(){const e=b("dev"),a=b(["design","data"]);return{single:e,multiple:a,domains:[{value:"design",label:"Design"},{value:"dev",label:"Développement"},{value:"produit",label:"Produit"},{value:"data",label:"Data"}]}},template:`
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
    `}),parameters:{controls:{disable:!0}}},I={name:"Supprimable",render:()=>({components:{CspTag:f},setup(){return{active:b(["Accessibilité","Vue","TypeScript"])}},template:`
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
    `}),parameters:{controls:{disable:!0}}},z={name:"États",render:()=>({components:{CspTag:f},template:`
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
    `}),parameters:{controls:{disable:!0}}};var O,H,U;S.parameters={...S.parameters,docs:{...(O=S.parameters)==null?void 0:O.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...(U=(H=S.parameters)==null?void 0:H.docs)==null?void 0:U.source}}};var K,$,W;w.parameters={...w.parameters,docs:{...(K=w.parameters)==null?void 0:K.docs,source:{originalSource:`{
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
}`,...(W=($=w.parameters)==null?void 0:$.docs)==null?void 0:W.source}}};var Z,J,Q;R.parameters={...R.parameters,docs:{...(Z=R.parameters)==null?void 0:Z.docs,source:{originalSource:`{
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
}`,...(Q=(J=R.parameters)==null?void 0:J.docs)==null?void 0:Q.source}}};var Y,X,ee;A.parameters={...A.parameters,docs:{...(Y=A.parameters)==null?void 0:Y.docs,source:{originalSource:`{
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
}`,...(ee=(X=A.parameters)==null?void 0:X.docs)==null?void 0:ee.source}}};var te,ae,se;V.parameters={...V.parameters,docs:{...(te=V.parameters)==null?void 0:te.docs,source:{originalSource:`{
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
}`,...(se=(ae=V.parameters)==null?void 0:ae.docs)==null?void 0:se.source}}};var re,ne,ie;_.parameters={..._.parameters,docs:{...(re=_.parameters)==null?void 0:re.docs,source:{originalSource:`{
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
}`,...(ie=(ne=_.parameters)==null?void 0:ne.docs)==null?void 0:ie.source}}};var le,oe,ce;I.parameters={...I.parameters,docs:{...(le=I.parameters)==null?void 0:le.docs,source:{originalSource:`{
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
}`,...(ce=(oe=I.parameters)==null?void 0:oe.docs)==null?void 0:ce.source}}};var de,pe,ue;z.parameters={...z.parameters,docs:{...(de=z.parameters)==null?void 0:de.docs,source:{originalSource:`{
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
}`,...(ue=(pe=z.parameters)==null?void 0:pe.docs)==null?void 0:ue.source}}};const vt=["Default","Variants","WithIcon","Sizes","Selectable","SelectableGroup","Dismissible","States"];export{S as Default,I as Dismissible,V as Selectable,_ as SelectableGroup,A as Sizes,z as States,w as Variants,R as WithIcon,vt as __namedExportsOrder,ht as default};
