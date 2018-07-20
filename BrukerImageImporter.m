
%% Bruker Image importer
clear all
close all

%% Read FID

% read in fid file as int32 with file header
[FID, FIDPATH] = uigetfile('*.*');
 fi=fopen([FIDPATH FID], 'rb', 'ieee-le');
[data, cnt]=fread(fi, inf,'int32');
fclose(fi);

% reshape the data and construct an array of complex numbers
  data2=reshape(data, 2, cnt/2);
  cdata=complex(data2(1,:), data2(2,:));
 
% now cdata is an array of complex number, you can reshape it for following fft reconstruction

%% Reconstruct
kspace_temp = reshape(cdata,128,128,80);
kspace_size = size(kspace_temp);

im_recon =  fftshift(fftn(fftshift(kspace_temp)))*1/sqrt(length(kspace_temp(:)));
im_recon = circshift(im_recon,-kspace_size(3)/2,3);

imagesc(abs(im_recon(:,:,40)))
colormap gray


%% Write image to file

data = uint16(abs(im_recon));
outputFileName = [FIDPATH 'matlabRecon.tif'];


for k = 1:size(data,3);
    imwrite(data(:,:,k),outputFileName,'writemode','append','compression','none')
end
