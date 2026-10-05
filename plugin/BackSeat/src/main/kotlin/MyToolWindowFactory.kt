package com.backseat

import com.intellij.openapi.Disposable
import com.intellij.openapi.editor.EditorFactory
import com.intellij.openapi.editor.event.DocumentEvent
import com.intellij.openapi.editor.event.DocumentListener
import com.intellij.openapi.fileEditor.FileDocumentManager
import com.intellij.openapi.fileEditor.FileEditorManager
import com.intellij.openapi.fileEditor.FileEditorManagerEvent
import com.intellij.openapi.fileEditor.FileEditorManagerListener
import com.intellij.openapi.project.Project
import com.intellij.openapi.vfs.VirtualFile
import com.intellij.openapi.wm.ToolWindow
import com.intellij.openapi.wm.ToolWindowFactory
import com.intellij.ui.components.JBScrollPane
import com.intellij.ui.components.JBTextArea
import com.intellij.ui.content.ContentFactory
import java.awt.BorderLayout
import javax.swing.JPanel

class MyToolWindowFactory : ToolWindowFactory {

    override fun shouldBeAvailable(project: Project) = true

    override fun createToolWindowContent(project: Project, toolWindow: ToolWindow) {
        toolWindow.stripeTitle = "Mortards"

        val mirror = MirrorPanel(project, toolWindow.disposable)
        val content = ContentFactory.getInstance().createContent(mirror.getContent(), "Mortards", false)
        toolWindow.contentManager.addContent(content)
    }

    class MirrorPanel(private val project: Project, parentDisposable: Disposable) {

        private val textArea = JBTextArea().apply {
            isEditable = false
            font = java.awt.Font("JetBrains Mono", java.awt.Font.PLAIN, 12)
            lineWrap = false
        }

        private val panel = JPanel(BorderLayout()).apply {
            add(JBScrollPane(textArea), BorderLayout.CENTER)
        }

        init {
            // Rebuild when files are opened/closed or the tab selection changes
            project.messageBus.connect(parentDisposable).subscribe(
                FileEditorManagerListener.FILE_EDITOR_MANAGER,
                object : FileEditorManagerListener {
                    override fun selectionChanged(event: FileEditorManagerEvent) = refresh()
                    override fun fileOpened(source: FileEditorManager, file: VirtualFile) = refresh()
                    override fun fileClosed(source: FileEditorManager, file: VirtualFile) = refresh()
                }
            )

            // One global listener covers edits in every document; refresh() only
            // shows documents that belong to currently open files.
            EditorFactory.getInstance().eventMulticaster.addDocumentListener(
                object : DocumentListener {
                    override fun documentChanged(event: DocumentEvent) = refresh()
                },
                parentDisposable
            )

            refresh()
        }

        private fun refresh() {
            val docManager = FileDocumentManager.getInstance()

            textArea.text = FileEditorManager.getInstance(project).openFiles
                .mapNotNull { file ->
                    docManager.getDocument(file)?.let { doc -> file to doc.text }
                }
                .joinToString("\n\n") { (file, text) ->
                    "===== ${file.path} =====\n$text"
                }
        }

        fun getContent(): JPanel = panel
    }
}