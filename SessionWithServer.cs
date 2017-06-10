using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Net.Sockets;
using System.Windows.Forms;
using System.Threading;
using System.IO;
using System.Security.Cryptography;
using System.Diagnostics;

namespace teacher_gui_windows_forms
{
    class SessionWithServer
    {
        private int localPort = 1027;
        private int localStreamPort = 1028;
        private string localHost = "127.0.0.1";
        private TeacherGUI form;
        public Socket guiCommandSocket;
        public Socket guiStreamSocket;
        public Socket streamSocket;
        public Socket commandSocket;
        private Process processPython;
        private int count = 1;
        StudentControl studentControl;

        public SessionWithServer(TeacherGUI form)
        {
            ///<summary>
            ///The structive function.
            ///</summary>
            ///<param name="form">The GUI.</param>
            
            processPython = new Process();
            processPython.StartInfo.FileName = @"C:\Heights\PortableApps\PortablePython2.7.6.1\Python-Portable.exe";
            processPython.StartInfo.Arguments = "multi_client_server.py";
            processPython.StartInfo.WorkingDirectory = Application.StartupPath;
            //processPython.StartInfo.WindowStyle = ProcessWindowStyle.Hidden;
            processPython.Start();

            this.form = form;

            IPEndPoint commandIPEndPoint = new IPEndPoint(IPAddress.Parse(localHost), localPort);
            guiCommandSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            guiCommandSocket.Bind(commandIPEndPoint);
            guiCommandSocket.Listen(1);

            IPEndPoint streamIPEndPoint = new IPEndPoint(IPAddress.Parse(localHost), localStreamPort);
            guiStreamSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            guiStreamSocket.Bind(streamIPEndPoint);
            guiStreamSocket.Listen(1);

            Console.WriteLine("waiting fot command socket to connect");
            commandSocket = guiCommandSocket.Accept();
            Console.WriteLine("command socket accepted");


            Thread waitingFotClients = new Thread(new ThreadStart(AddClient));
            waitingFotClients.Start();
            Console.WriteLine("Thread started");
        }

        public void AddClient()
        {
            ///<summary>
            ///A function for a Threads.
            ///The streamSocket waits for a new client to connect.
            ///Connects another client with the server for stream.
            ///And starts the stream for the client with a thread.
            ///</summary>
            ///<returns>Void</returns>

            byte[] clientIP = new byte[32];

            while (true)
            {
                Console.WriteLine("waiting for client");
                streamSocket = guiStreamSocket.Accept();
                Console.WriteLine("client accepted");

                streamSocket.Receive(clientIP);
                string stringIP = Encoding.Default.GetString(clientIP);
                Console.WriteLine("got client's ip: " + stringIP);

                Thread.Sleep(50);
                AddImage(stringIP);

                ForStream SocketToUse = new ForStream(streamSocket, this);
                Thread stream = new Thread(new ThreadStart(SocketToUse.GetStream));
                stream.Start();
            }
        }

        public Image GetAnImage()
        {
            byte[] lenOfImage = new byte[7];
            byte[] temporaryData = new byte[1024];
            byte[] encodedImg = new byte[0];
            int bytesReceived = 0;

            try
            {
                streamSocket.Receive(lenOfImage, 0, 7, SocketFlags.None);
                int imageLength = Convert.ToInt32(Encoding.Default.GetString(lenOfImage));
                Array.Resize(ref encodedImg, imageLength);
                while (bytesReceived < imageLength)
                {
                    bytesReceived += streamSocket.Receive(encodedImg, bytesReceived, Math.Min(1024, imageLength - bytesReceived), SocketFlags.None);
                }

                using (var ms = new MemoryStream(encodedImg))
                {
                    var x = Image.FromStream(ms);
                    return Image.FromStream(ms);
                }
            }
            catch
            {
                return null;
            }
        }

        public void AddImage(string ip)
         {
            ///<summary>
            ///When a new client is added his image is added
            ///to the ImageList thus appear on the gui.
            ///</summary>
            ///<param name="ip">An ip of a client in string.</param>
            ///<returns>Void</returns>
            Console.WriteLine("adding image");
            Image image = GetAnImage();
            form.Invoke(new MethodInvoker(delegate
            {
                studentControl = new StudentControl(image, ip, count++);
                form.studentBox.Controls.Add(studentControl);
            }));
        }

        public void ChangeImage(Image image, string ip)
        {
            ///<summary>
            ///Whenever a new image is received, this function changes the client's image to the current image.
            ///</summary>
            ///<param name="image">An image.</param>
            ///<param name="ip">An ip of a client.</param>
            ///<returns>Void</returns>
  
            form.Invoke(new MethodInvoker(delegate
            {
                foreach (Control control in form.studentBox.Controls)
                {
                    StudentControl studentControl = control as StudentControl;
                    if (studentControl.labelIp.Text.Equals(ip))
                    {
                        if(studentControl.studentForm != null)
                        {
                            studentControl.studentForm.ChangeImage(image);
                        }
                        studentControl.ChangeImage(image);
                        break;
                    }
                }
            }));
        }

    }

    class ForStream
    {
        //This class if for the thread get stream to use.
        Socket streamSocket;
        SessionWithServer mainClass;

        public ForStream(Socket streamSocket, SessionWithServer mainClass)
        {
            this.streamSocket = streamSocket;
            this.mainClass = mainClass;
        }

        public void GetStream()
        {
            byte[] clientIP = new byte[32];
            while (true)
            {
                try
                {
                    int len = streamSocket.Receive(clientIP);
                    string lenStr = Encoding.Default.GetString(clientIP).Substring(0, len);
                    Image img = mainClass.GetAnImage();
                    mainClass.ChangeImage(img, lenStr);
                }
                catch
                {
                    
                }
            }
        }
    }
}
