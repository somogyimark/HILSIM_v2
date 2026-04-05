export default {
    template: `<div ref="editorContainer" class="w-full h-full text-left"></div>`,
    props: {
        value: String,
        dark_mode: Boolean,
    },
    mounted() {
        // Ha már betöltött, csak inicializálunk
        if (window.monaco) {
            this.initMonaco();
            return;
        }
        // Különben letöltjük a VS Code (Monaco) motorját
        const script = document.createElement('script');
        script.src = '/monaco-vs/loader.js';
        document.head.appendChild(script);
        script.onload = () => {
            window.require.config({ paths: { 'vs': '/monaco-vs' } });

            window.require(['vs/editor/editor.main'], () => {
                this.initMonaco();
            });
        };
    },
    methods: {
        initMonaco() {
            // 1. Saját nyelv regisztrálása
            if (!monaco.languages.getLanguages().some(l => l.id === 'hilsim')) {
                monaco.languages.register({ id: 'hilsim' });

                // 2. Szintaxis kiemelés (Színezés)
                monaco.languages.setMonarchTokensProvider('hilsim', {
                    tokenizer: {
                        root: [
                            [/batchControl/, 'keyword'],          // Kulcsszó (Kék)
                            [/-[a-zA-Z]+/, 'type'],               // Paraméterek (Lila)
                            [/\d+/, 'number'],                    // Számok (Zöldes)
                            [/\/\/.*$/, 'comment'],               // Kommentek (Zöld)
                            [/".*"/, 'string'],                   // Szövegek (Narancs)
                            [/(temp|rpm|switch|on|off)/, 'variable'], // Változók (Világoskék)
                        ]
                    }
                });

                // 3. Autocomplete (Kiegészítések)
                monaco.languages.registerCompletionItemProvider('hilsim', {
                    provideCompletionItems: () => {
                        const suggestions = [
                            { label: 'batchControl', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'batchControl ' },
                            { label: '-init', kind: monaco.languages.CompletionItemKind.Function, insertText: '-init' },
                            { label: '-hwfi', kind: monaco.languages.CompletionItemKind.Function, insertText: '-hwfi ' },
                            { label: '-start', kind: monaco.languages.CompletionItemKind.Function, insertText: '-start' },
                            { label: '-wait', kind: monaco.languages.CompletionItemKind.Function, insertText: '-wait ' },
                            { label: '-log', kind: monaco.languages.CompletionItemKind.Function, insertText: '-log "$1"' },
                            { label: '-getHilState', kind: monaco.languages.CompletionItemKind.Function, insertText: '-getHilState' },
                            { label: '-bug_on', kind: monaco.languages.CompletionItemKind.Function, insertText: '-bug_on'},
                            { label: 'pause', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'pause' },
                        ];
                        return { suggestions: suggestions };
                    }
                });

                // 4. A saját sötét dizájnod beállítása
                monaco.editor.defineTheme('hilsim-dark', {
                    base: 'vs-dark',
                    inherit: true,
                    rules: [
                        { token: 'keyword', foreground: '569cd6', fontStyle: 'bold' },
                        { token: 'type', foreground: 'c586c0' },
                        { token: 'variable', foreground: '9cdcfe' },
                        { token: 'comment', foreground: '6a9955', fontStyle: 'italic' },
                        { token: 'string', foreground: 'ce9178' }
                    ],
                    colors: {
                        'editor.background': '#0b1426', // A dashboardod sötétkék háttere!
                    }
                });

                monaco.editor.defineTheme('hilsim-light', {
                    base: 'vs',
                    inherit: true,
                    rules: [
                        { token: 'keyword', foreground: '0000ff', fontStyle: 'bold' },
                        { token: 'type', foreground: 'af00db' },
                        { token: 'variable', foreground: '0070c1' },
                        { token: 'comment', foreground: '008000', fontStyle: 'italic' },
                        { token: 'string', foreground: 'a31515' }
                    ],
                    colors: {
                        'editor.background': '#f9fafb',
                    }
                });
            }

            // Editor létrehozása
            this.editor = monaco.editor.create(this.$refs.editorContainer, {
                value: this.value,
                language: 'hilsim',
                theme: this.dark_mode ? 'hilsim-dark' : 'hilsim-light',
                automaticLayout: true,
                minimap: { enabled: false },
                overviewRulerLanes: 0,
                scrollBeyondLastLine: false,
                fontSize: 14
            });

            // Változás figyelése és küldése a Pythonnak
            this.editor.onDidChangeModelContent(() => {
                this.$emit('update:value', this.editor.getValue());
            });
        }
    },
    watch: {
        // Ha a Python kód változtatja meg a szöveget, frissüljön az Editor
        value(newValue) {
            if (this.editor && newValue !== this.editor.getValue()) {
                this.editor.setValue(newValue);
            }
        },
        dark_mode(newValue) {
            if (window.monaco) {
                monaco.editor.setTheme(newValue ? 'hilsim-dark' : 'hilsim-light');
            }
        }
    },
    beforeUnmount() {
        if (this.editor) this.editor.dispose();
    }
};