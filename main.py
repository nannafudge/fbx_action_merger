import tkinter as tk
from tkinter import ttk, filedialog

import fbx
import FbxCommon
from pyfbx import *

from fbx import FbxSkeleton
from fbx import FbxAnimLayer

import os

from pyfbx.fbox import FBox


class FbxActionMergerGui:
    animations = []
    skeletons = []

    scenes = []

    def __init__(self, window):
        self.window = window
        window.title("FBX Action Merger")

        self.layout = tk.PanedWindow(orient=tk.HORIZONTAL)
        self.layout.pack(fill=tk.BOTH, expand=1)

        self.leftLabelOpenFile = tk.LabelFrame(self.layout, text="Load FBX Files", padx=5, pady=5)
        self.leftLabelOpenFile.pack(padx=10, pady=10, fill=tk.BOTH, expand=1)
        self.layout.add(self.leftLabelOpenFile)

        self.openFileButton = tk.Button(self.leftLabelOpenFile, text="Browse", command=self.openFileDialog)
        self.openFileButton.grid(column=1, row=1)
        self.openFileButton.pack()

        self.leftTreeView = ttk.Treeview(self.leftLabelOpenFile, selectmode=tk.BROWSE)
        self.leftTreeView["columns"] = ("file", "skeleton", "animations")

        self.leftTreeView.heading("file", text="File")
        self.leftTreeView.heading("skeleton", text="Skeleton")
        self.leftTreeView.heading("animations", text="Animations")

        self.leftTreeView.column("file", minwidth=128, stretch=True)
        self.leftTreeView.column("skeleton", minwidth=128, stretch=True)
        self.leftTreeView.column("animations", minwidth=128, stretch=True)
        self.leftTreeView.pack(fill=tk.BOTH, expand=1)

        self.rightPreviewFrame = tk.LabelFrame(self.layout, text="FBX Result", padx=5, pady=5)
        self.rightPreviewFrame.pack(padx=10, pady=10, fill=tk.BOTH, expand=1)
        self.layout.add(self.rightPreviewFrame)

        self.skeleton = tk.Variable(self.rightPreviewFrame)
        self.skeleton.set(None)

        self.selectedArmature = ttk.OptionMenu(self.rightPreviewFrame, self.skeleton, *self.skeletons)
        self.selectedArmature.pack(fill=tk.X)

        self.saveFileButton = tk.Button(self.rightPreviewFrame, text="Save", command=self.packFbxAnimations)
        self.saveFileButton.pack()

        self.animationList = ttk.Treeview(self.rightPreviewFrame, selectmode=tk.EXTENDED, columns=["animation"],
                                          displaycolumns=["animation"])
        self.animationList.heading("animation", text="Animation")
        self.animationList.column("animation", minwidth=128, stretch=True)
        self.animationList.pack(fill=tk.BOTH, expand=1)

        # if result:
        #    animations = scene.GetCurrentAnimationStack()
        #    self.leftTreeView.insert('', 'end', text='fak')

    def openFileDialog(self):
        files = filedialog.askopenfilenames(initialdir=".", title="Select FBX Files",
                                            filetypes=[('Autodesk FBX Files', '.fbx')])

        if files:
            for i in self.leftTreeView.get_children():
                self.leftTreeView.delete(i)

            self.animations.clear()
            self.skeletons.clear()
            self.scenes.clear()

        fbox = FBox()

        for file in files:
            short_filename = os.path.basename(file)

            manager = pyfbx.Manager()
            scene = pyfbx.Scene(manager, short_filename)
            result = pyfbx.loadScene(manager, scene, short_filename)

            if result:
                animation_stack = scene._me.GetCurrentAnimationStack()

                local_skeletons = []
                local_animations = []

                #for i in range(lNode.GetChildCount()):
                #    if type(lNode.GetChild(i).GetNodeAttribute()) is FbxSkeleton:
                #        local_skeletons.append(lNode.GetChild(i).GetNodeAttribute())

                #for i in range(animation_stack.GetMemberCount()):
                #    if type(animation_stack.GetMember(i)) is FbxAnimLayer:
                #        local_animations.append(animation_stack.GetMember(i))

                short_filename = os.path.basename(file)

                self.skeletons += local_skeletons
                self.animations += local_animations

                subtree = self.leftTreeView.insert("", "end", file,
                                                   values=(short_filename, len(local_skeletons), local_animations))
                for skeleton in local_skeletons:
                    skeleton_name = skeleton.GetName()
                    if skeleton_name == "":
                        skeleton_name = "Unnamed"

                    skeleton_subtree = self.leftTreeView.insert(subtree, "end",
                                                                values=(u'↳', skeleton_name, local_animations))

                    for animation in local_animations:
                        self.leftTreeView.insert(skeleton_subtree, "end", values=("", u'↳', animation.GetName()))

        self.selectedArmature.set_menu(*self.skeletons)

        for i in self.animationList.get_children():
            self.animationList.delete(i)

        self.animationList.set_children("", *self.animations)

        # CREATE POPUP WINDOW CLASS
        # MAKE POPUP WINDOW CLASS AWARE OF CID OF THE RIGHT CLICKED ENTITY

    def packFbxAnimations(self):
        pass

    def setSkeleton(self, event):
        pass

    def selectArmature(self):
        pass


def main():
    window = tk.Tk()
    gui = FbxActionMergerGui(window)
    window.mainloop()

    manager = pyfbx.Manager()


if __name__ == "__main__":
    main()
