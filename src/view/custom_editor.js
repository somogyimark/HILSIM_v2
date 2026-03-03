export default {
    template: `<div ref="editorContainer" class="w-full h-full text-left"></div>`,
    props: {
        value: String,
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
                            { label: 'temp', kind: monaco.languages.CompletionItemKind.Variable, insertText: 'temp' },
                            { label: 'rpm', kind: monaco.languages.CompletionItemKind.Variable, insertText: 'rpm' },
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
            }

            // Editor létrehozása
            this.editor = monaco.editor.create(this.$refs.editorContainer, {
                value: this.value,
                language: 'hilsim',
                theme: 'hilsim-dark',
                automaticLayout: true,
                minimap: { enabled: false },
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
        }
    },
    beforeUnmount() {
        if (this.editor) this.editor.dispose();
    }
};