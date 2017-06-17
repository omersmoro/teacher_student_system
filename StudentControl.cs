using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace teacher_gui_windows_forms
{
    public partial class StudentControl : UserControl
    {
        const int Num = 10;
        string message;
        public StudentForm studentForm = null;
        private TeacherGUI form;

        public StudentControl(TeacherGUI form, Image image, string Ip, int index)
        {
            InitializeComponent();
            this.form = form;
            pictureBoxImage.Image = image;
            labelIp.Text = Ip;
            Location = new Point(index % Num * (Width + 10) - Width, index / Num * (Height + 5) + 30);
        }

        public void ChangeImage(Image image)
        {
            pictureBoxImage.Image = image;
        }

        private void StudentControl_Click(object sender, EventArgs e)
        {
            studentForm = new StudentForm(pictureBoxImage.Image, labelIp.Text);
            studentForm.ShowDialog();
        }

        private void pictureBoxImage_Click(object sender, EventArgs e)
        {
            studentForm = new StudentForm(pictureBoxImage.Image, labelIp.Text);
            studentForm.ShowDialog();
        }

        private void labelIp_Click(object sender, EventArgs e)
        {
            studentForm = new StudentForm(pictureBoxImage.Image, labelIp.Text);
            studentForm.ShowDialog();
        }


        private void controlToolStripMenuItem_Click_1(object sender, EventArgs e)
        {
            form.session.commandSocket.Send(Encoding.ASCII.GetBytes(labelIp.Text+ "#control"));
        }
    }
}
