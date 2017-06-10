namespace teacher_gui_windows_forms
{
    partial class StudentControl
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

        #region Component Designer generated code

        /// <summary> 
        /// Required method for Designer support - do not modify 
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.pictureBoxImage = new System.Windows.Forms.PictureBox();
            this.labelIp = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxImage)).BeginInit();
            this.SuspendLayout();
            // 
            // pictureBoxImage
            // 
            this.pictureBoxImage.Location = new System.Drawing.Point(0, 0);
            this.pictureBoxImage.Name = "pictureBoxImage";
            this.pictureBoxImage.Size = new System.Drawing.Size(150, 126);
            this.pictureBoxImage.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pictureBoxImage.TabIndex = 0;
            this.pictureBoxImage.TabStop = false;
            this.pictureBoxImage.Click += new System.EventHandler(this.pictureBoxImage_Click);
            // 
            // labelIp
            // 
            this.labelIp.Location = new System.Drawing.Point(15, 129);
            this.labelIp.Name = "labelIp";
            this.labelIp.Size = new System.Drawing.Size(119, 23);
            this.labelIp.TabIndex = 1;
            this.labelIp.Text = "label1";
            this.labelIp.Click += new System.EventHandler(this.labelIp_Click);
            // 
            // StudentControl
            // 
            this.Controls.Add(this.labelIp);
            this.Controls.Add(this.pictureBoxImage);
            this.Name = "StudentControl";
            this.Size = new System.Drawing.Size(150, 158);
            this.Click += new System.EventHandler(this.StudentControl_Click);
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxImage)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.PictureBox pictureBoxImage;
        public System.Windows.Forms.Label labelIp;
    }
}
