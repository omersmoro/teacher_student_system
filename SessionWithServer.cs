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
        private string localHost = "127.0.0.1";
        private List<IPEndPoint> clientsIPEndPoints = new List<IPEndPoint>();
        private TeacherGUI form;
        private Socket mainSocket;

        public SessionWithServer(TeacherGUI form)
        {
            ///<summary>
            ///The structive function.
            ///</summary>
            ///<param name="form">The GUI..</param>
            mainSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            mainSocket.Connect(localHost, localPort);
            this.form = form;
        }

        public void AddClient()
        {
            ///<summary>
            ///Connects another socket for another client with the server.
            ///Adds the socket to the clientsSockets.
            ///</summary>
            ///<returns>Void</returns>
            IPEndPoint IPAndPort = new IPEndPoint(Convert.ToInt64(localHost), localPort);
            UdpClient clientSocket = new UdpClient(IPAndPort);
            IPEndPoint sender = new IPEndPoint(IPAddress.Any, localPort);
            clientSocket.Receive(ref sender);

            clientsIPEndPoints.Add(sender);
            AddImage(sender);
            ForStream SocketToUse = new ForStream(clientSocket, this);
            Thread stream = new Thread(new ThreadStart(SocketToUse.GetStream));
            stream.Start();
        }

        public Image GetAnImage(Socket clientSOcket, IPEndPoint clientIPEndPoint)
        {
            byte[] lenOfImage = new byte[7];
            byte[] encodedImg = new byte[0];

            lenOfImage = clientSocket.Receive(clientIPEndPoint);
            Array.Resize(ref encodedImg, BitConverter.ToInt32(lenOfImage, 0));
            clientSocket.Receive(encodedImg, 0, 1024, SocketFlags.None);
            int offsetOfBuffer = 1024;
            int lengthOfImg = BitConverter.ToInt32(encodedImg, 0);

            while (encodedImg.Length + 1024 < lengthOfImg)
            {
                clientSocket.Receive(encodedImg, offsetOfBuffer, 1024, SocketFlags.None);
                offsetOfBuffer += 1024;
                lengthOfImg = BitConverter.ToInt32(encodedImg, 0);
            }

            clientSocket.Receive(encodedImg, offsetOfBuffer, BitConverter.ToInt32(encodedImg, 0) - lengthOfImg, SocketFlags.None);
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

        private void AddImage(IPEndPoint clientSocket)
        {
            ///<summary>
            ///When a new client is added his image is added
            ///to the ImageList thus appear on the gui.
            ///</summary>
            ///<param name="image">An image.</param>
            ///<returns>Void</returns>
            byte[] ipArray = new byte[32];
            clientSocket.Receive(ipArray);
            string ip = BitConverter.ToString(ipArray);
            Image image = GetAnImage(clientSocket);
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
        SessionWithServer s;

        public ForStream(Socket clientSocket, SessionWithServer s)
        {
            this.clientSocket = clientSocket;
            this.s = s;
        }

        public void GetStream()
        {
            byte[] lenOfImage = new byte[7];
            byte[] encodedImg = new byte[0];
            byte[] ipArray = new byte[32];
            while (true)
            {
                clientSocket.Receive(ipArray);
                Image img = s.GetAnImage(clientSocket);
                s.ChangeImage(img, BitConverter.ToString(ipArray));
            }
        }
    }
}
