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

namespace teacher_gui_windows_forms
{
    class SessionWithServer
    {
        private int localPort = 1027;
        private int streamPort = 1029;
        private string localHost = "127.0.0.1";
        private TeacherGUI form;
        private Socket mainSocket;
        private Socket serverStreamSocket;
        private Socket clientStreamSocket;

        public SessionWithServer(TeacherGUI form)
        {
            ///<summary>
            ///The structive function.
            ///</summary>
            ///<param name="form">The GUI..</param>
            mainSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            mainSocket.Connect(localHost, streamPort);

            serverStreamSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            serverStreamSocket.Listen(1);

            this.form = form;
        }

        public void AddClient()
        {
            ///<summary>
            ///Connects another socket for another client with the server.
            ///Adds the socket to the clientsSockets.
            ///</summary>
            ///<returns>Void</returns>
            
            byte[] clientIP = new byte[32];

            clientStreamSocket = serverStreamSocket.Accept();

            clientStreamSocket.Receive(clientIP);
            AddImage(BitConverter.ToString(clientIP));

            ForStream SocketToUse = new ForStream(clientStreamSocket, this);
            Thread stream = new Thread(new ThreadStart(SocketToUse.GetStream));
            stream.Start();
        }

        public Image GetAnImage()
        {
            byte[] lenOfImage = new byte[7];
            byte[] temporaryData = new byte[1024];
            byte[] encodedImg = new byte[0];
            int offsetOfBuffer = 0;

            clientStreamSocket.Receive(lenOfImage);
            Array.Resize(ref encodedImg, BitConverter.ToInt32(lenOfImage, 0));

            clientStreamSocket.Receive(temporaryData, offsetOfBuffer, 1024, SocketFlags.None);
            for(int i=offsetOfBuffer; i<offsetOfBuffer+1024; i++)
            {
                encodedImg[i] = temporaryData[i];
            }
            offsetOfBuffer += 1024;
            while (encodedImg.Count() + 1024 < BitConverter.ToInt32(lenOfImage, 0))
            {
                clientStreamSocket.Receive(temporaryData, offsetOfBuffer, 1024, SocketFlags.None);
                for (int i = offsetOfBuffer; i < offsetOfBuffer + 1024; i++)
                {
                    encodedImg[i] = temporaryData[i];
                }
                offsetOfBuffer += 1024;
            }

            clientStreamSocket.Receive(encodedImg, offsetOfBuffer, BitConverter.ToInt32(encodedImg, 0) - encodedImg.Count(), SocketFlags.None);

            byte[] decodedImg = Convert.FromBase64String(Encoding.Default.GetString(encodedImg));
            Image img = ConvertByteArrayToImage(decodedImg);
            return img;
        }

        private Image ConvertByteArrayToImage(byte[] byteArrayImg)
        {
            MemoryStream msImage = new MemoryStream(byteArrayImg);
            Image theImage = Image.FromStream(msImage);
            msImage.Dispose();
            return theImage;
        }
        
        public void AddImage(string ip)
        {
            ///<summary>
            ///When a new client is added his image is added
            ///to the ImageList thus appear on the gui.
            ///</summary>
            ///<param name="image">An image.</param>
            ///<returns>Void</returns>
            Image image = GetAnImage();
            form.ImageList1.Images.Add(image);
            form.ListView1.Items.Add(new ListViewItem(ip, form.ImageList1.Images.Count - 1));
        }

        public void ChangeImage(Image image, string ip)
        {
            ///<summary>
            ///Whenever a new image is received, this function changes the client's image to the current image.
            ///</summary>
            ///<param name="image">An image.</param>
            ///<param name="ip">Am ip of a client.</param>
            ///<returns>Void</returns>
            int i = 0;
            foreach (ListViewItem item in form.ListView1.Items)
            {
                if (item.Text.Equals(ip))
                {
                    form.ImageList1.Images[i] = image;
                    break;
                }
                i++;
            }

        }

    }

    class ForStream
    {
        //This class if for the thread get stream to use.
        Socket clientSocket;
        SessionWithServer mainClass;

        public ForStream(Socket clientSocket, SessionWithServer mainClass)
        {
            this.clientSocket = clientSocket;
            this.mainClass = mainClass;
        }

        public void GetStream()
        {
            byte[] clientIP = new byte[32];
            while (true)
            {
                clientSocket.Receive(clientIP);
                Image img = mainClass.GetAnImage();
                mainClass.ChangeImage(img, BitConverter.ToString(clientIP));
            }
        }
    }
}
