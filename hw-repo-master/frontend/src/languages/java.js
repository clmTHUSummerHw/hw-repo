import { language as java } from 'monaco-editor/esm/vs/basic-languages/java/java';
import * as monaco from 'monaco-editor';

export default {
	setup()
	{
		monaco.languages.registerCompletionItemProvider('java', {
			provideCompletionItems: function ()
			{
				let suggestions = [];
				java.keywords.forEach(item =>
				{
					suggestions.push({
						label: item,
						kind: monaco.languages.CompletionItemKind.Keyword,
						insertText: item
					});
				})
				return {
					suggestions: suggestions
				};
			},
		});
	}
}