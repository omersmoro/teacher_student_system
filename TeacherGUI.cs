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
    public partial class TeacherGUI : Form
    {           
        SessionWithServer session;

        public TeacherGUI()
        {
            InitializeComponent();
            session = new SessionWithServer(this);
        }

        private void TeacherGUI_Load(object sender, EventArgs e)
        {
            studentBox.Width = Width;
            studentBox.Height = Height / 2;
            studentBox.Top = Height - studentBox.Height;
        }
    }
}