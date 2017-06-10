using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace teacher_gui_windows_forms
{
    public partial class StudentForm : Form
    {
        public StudentForm(Image image, string studentIp)
        {
            InitializeComponent();
            pictureBoxImage.Image = image;
            Text = studentIp;
        }

        public void ChangeImage(Image image)
        {
            pictureBoxImage.Image = image;
        }
    }
}