﻿namespace teacher_gui_windows_forms
{
    partial class TeacherGUI
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.studentBox = new System.Windows.Forms.GroupBox();
            this.SuspendLayout();
            // 
            // studentBox
            // 
            this.studentBox.BackColor = System.Drawing.SystemColors.ControlLightLight;
            this.studentBox.Location = new System.Drawing.Point(0, 297);
            this.studentBox.Name = "studentBox";
            this.studentBox.Size = new System.Drawing.Size(1459, 357);
            this.studentBox.TabIndex = 2;
            this.studentBox.TabStop = false;
            this.studentBox.Text = "Students";
            // 
            // TeacherGUI
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1459, 666);
            this.Controls.Add(this.studentBox);
            this.Name = "TeacherGUI";
            this.Text = "TeacherGUI";
            this.WindowState = System.Windows.Forms.FormWindowState.Maximized;
            this.Load += new System.EventHandler(this.TeacherGUI_Load);
            this.ResumeLayout(false);

        }

        #endregion
        public System.Windows.Forms.GroupBox studentBox;
    }
}