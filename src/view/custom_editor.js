export default {
    template: `<div ref="editorContainer" class="w-full h-full text-left"></div>`,
    props: {
        value: String,
        dark_mode: Boolean,
    },
    mounted() {
        if (window.monaco) {
            this.initMonaco();
            return;
        }
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
            if (!monaco.languages.getLanguages().some(l => l.id === 'hilsim')) {
                monaco.languages.register({ id: 'hilsim' });

                monaco.languages.setMonarchTokensProvider('hilsim', {
                    tokenizer: {
                        root: [
                            [/batchControl/, 'keyword'],
                            [/-[a-zA-Z]+/, 'type'],
                            [/\d+/, 'number'],
                            [/\/\/.*$/, 'comment'],
                            [/".*"/, 'string'],
                            [/(temp|rpm|switch|on|off)/, 'variable'],
                        ]
                    }
                });

                monaco.languages.registerCompletionItemProvider('hilsim', {
                    provideCompletionItems: () => {
                        const suggestions = [
                            { label: 'batchControl', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'batchControl ' },
                            { label: '-init', kind: monaco.languages.CompletionItemKind.Function, insertText: '-init' },
                            { label: '-hwfi', kind: monaco.languages.CompletionItemKind.Function, insertText: '-hwfi ' },
                            { label: '-swfi', kind: monaco.languages.CompletionItemKind.Function, insertText: '-swfi ' },
                            { label: '-start', kind: monaco.languages.CompletionItemKind.Function, insertText: '-start' },
                            { label: '-wait', kind: monaco.languages.CompletionItemKind.Function, insertText: '-wait ' },
                            { label: '-getHilState', kind: monaco.languages.CompletionItemKind.Function, insertText: '-getHilState' },
                            { label: '-bug_on', kind: monaco.languages.CompletionItemKind.Function, insertText: '-bug_on' },
                            { label: '-assert', kind: monaco.languages.CompletionItemKind.Function, insertText: '-assert' },
                            { label: 'pause', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'pause' },
                            { label: 'temp', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'temp' },
                            { label: 'pot', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'pot' },
                            { label: 'switch', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'switch' },
                            { label: 'temp_led', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'temp_led' },
                            { label: 'pot_led', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'pot_led' },
                            { label: 'switch_led', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'switch_led' },
                        ];
                        return { suggestions: suggestions };
                    }
                });

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
                        'editor.background': '#0b1426',
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

            this.editor.onDidChangeModelContent(() => {
                if (this.isSettingValue) return;
                const val = this.editor.getValue();
                if (!this.recentEmits) this.recentEmits = new Set();
                this.recentEmits.add(val);
                setTimeout(() => {
                    this.recentEmits.delete(val);
                }, 2000);
                this.$emit('update:value', val);
            });
        }
    },
    watch: {
        value(newValue) {
            if (this.editor && newValue !== this.editor.getValue()) {
                if (this.recentEmits && this.recentEmits.has(newValue)) {
                    return;
                }
                this.isSettingValue = true;
                this.editor.setValue(newValue);
                this.isSettingValue = false;
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